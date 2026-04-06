#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse
import csv
import io
import os
import socket
import struct
import sys
import time
from datetime import datetime
from threading import Event, Thread

# Ensure pymodbus v1.x for Python 2
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException


# ----------- Low-level helpers ------------------------------------------------

def f32_from_regs(hi, lo):
    """Big-endian 32-bit float from two 16-bit registers (hi, lo)."""
    try:
        return struct.unpack('>f', struct.pack('>HH', int(hi) & 0xFFFF, int(lo) & 0xFFFF))[0]
    except Exception:
        return float('nan')

def u32_from_regs(hi, lo):
    """Big-endian 32-bit unsigned int from two 16-bit registers (hi, lo)."""
    try:
        return struct.unpack('>I', struct.pack('>HH', int(hi) & 0xFFFF, int(lo) & 0xFFFF))[0]
    except Exception:
        return 0

def bits_set_0_31(val):
    """Return list of bit positions (0..31) that are set in val."""
    v = int(val) & 0xFFFFFFFF
    return [i for i in range(32) if (v >> i) & 1]

def safe_float(v):
    try:
        return float(v)
    except Exception:
        return v  # leave as-is if not numeric


# ----------- CompressorControl ------------------------------------------------

class CompressorControl(object):
    """
    Robust Cryomech compressor Modbus TCP interface (Python 2 compatible).

    - Reads a block of input registers (configurable start/count).
    - Decodes 16-bit, 32-bit floats, and 32-bit bitfields.
    - Extensible via REGMAP: add new parameters without touching updateData().
    """

    # type: "u16" (single 16-bit), "f32" (float32 using hi,lo), "u32" (bitfield/raw 32-bit)
    # scale is applied to numeric results afterwards (keep 1.0 if already scaled).
    REGMAP = {
        # --- core states (adjust per your manual if these are actually 16-bit) ---
        "operating_state"    : ("u16",  0,  0, 1.0),
        "compressor_running" : ("u16",  1,  1, 1.0),

        # These are bitfields on most Cryomech maps → treat as u32 (hi,lo indices!)
        "warning_state_raw"  : ("u32",  4,  3, 1.0),
        "alarm_state_raw"    : ("u32",  6,  5, 1.0),

        # Temps (°C) and pressures — your data suggests direct float32
        "coolant_in_temp"    : ("f32",  8,  7, 1.0),
        "coolant_out_temp"   : ("f32", 10,  9, 1.0),
        "oil_temp"           : ("f32", 12, 11, 1.0),
        "helium_temp"        : ("f32", 14, 13, 1.0),

        "low_pressure"       : ("f32", 16, 15, 1.0),
        "low_pressure_avg"   : ("f32", 18, 17, 1.0),
        "high_pressure"      : ("f32", 20, 19, 1.0),
        "high_pressure_avg"  : ("f32", 22, 21, 1.0),
        "delta_pressure_avg" : ("f32", 24, 23, 1.0),
        "motor_current"      : ("f32", 26, 25, 1.0),
        "operating_hours"    : ("f32", 28, 27, 1.0),

        # --- add more mapped values here once you have real indices from Cryomech map ---
        # "water_in_temp"     : ("f32", 30, 29, 1.0),
        # "water_out_temp"    : ("f32", 32, 31, 1.0),
        # "water_flow_lpm"    : ("f32", 34, 33, 1.0),
        # "cabinet_temp"      : ("f32", 36, 35, 1.0),
        # "input_power_kw"    : ("f32", 38, 37, 1.0),
        # "motor_speed_rpm"   : ("f32", 40, 39, 1.0),
    }

    # Example bit labels (placeholder; replace with vendor docs when available)
    WARNING_BITS = {
        0: "water_flow_low",
        1: "water_temp_high",
        2: "oil_temp_high",
        3: "low_pressure_high",
        4: "high_pressure_high",
        5: "helium_temp_high",
        6: "filter_dp_high",
        7: "cabinet_temp_high",
        # If your sample shows bit 31 set, you can add:
        # 31: "summary_warning",
    }

    ALARM_BITS = {
        0: "water_flow_fail",
        1: "overpressure_trip",
        2: "overtemp_trip",
        3: "vfd_fault",
        4: "phase_loss",
        5: "sensor_fault",
        6: "oil_level_low",
        7: "emergency_stop",
        # 31: "summary_alarm",
    }

    def __init__(self, addr, unit=16, port=502, timeout=3.0, auto_connect=True,
                 start=0, count=35, retries=3, retry_sleep=0.2):
        self.IP = addr
        self.unit = int(unit)
        self.start = int(start)
        self.count = int(count)
        self.retries = int(retries)
        self.retry_sleep = float(retry_sleep)
        self.client = ModbusTcpClient(self.IP, port=port, timeout=timeout)
        self.result = None
        self.data = {}
        if auto_connect:
            self.client.connect()

    def close(self):
        try:
            self.client.close()
        except Exception:
            pass

    def __del__(self):
        self.close()

    # ---- IO ----

    def _read_block(self):
        last_exc = None
        for _ in range(self.retries):
            try:
                res = self.client.read_input_registers(self.start, self.count, unit=self.unit)
                if (res is None) or isinstance(res, ModbusIOException) or (not hasattr(res, "registers")):
                    last_exc = ModbusIOException("Invalid/empty Modbus response")
                else:
                    return res
            except (socket.timeout, OSError) as e:
                last_exc = e
            time.sleep(self.retry_sleep)
        if last_exc:
            raise last_exc
        raise ModbusIOException("Failed to read registers")

    def readInputRegisters(self):
        self.result = self._read_block()
        return self.result

    # ---- Decode ----

    def _decode_by_map(self, regs):
        out = {}
        n = len(regs)
        for name, spec in self.REGMAP.iteritems():
            typ, hi_idx, lo_idx, scale = spec
            try:
                if typ == "u16":
                    if 0 <= hi_idx < n:
                        out[name] = float(regs[hi_idx]) * float(scale)
                elif typ == "f32":
                    if 0 <= hi_idx < n and 0 <= lo_idx < n:
                        out[name] = f32_from_regs(regs[hi_idx], regs[lo_idx]) * float(scale)
                elif typ == "u32":
                    if 0 <= hi_idx < n and 0 <= lo_idx < n:
                        out[name] = u32_from_regs(regs[hi_idx], regs[lo_idx])
            except Exception:
                # ignore bad decode; leave key absent
                pass
        return out

    def _decode_flags(self, raw_val, bitmap):
        """
        Return dict with:
          'flags': {label: bool}, and
          'unknown_bits': [bit_index,...] for any set bits not labeled.
        """
        if raw_val is None:
            return {"flags": {}, "unknown_bits": []}
        set_bits = bits_set_0_31(raw_val)
        flags = {}
        for bit, label in bitmap.iteritems():
            flags[label] = (bit in set_bits)
        unknown = [b for b in set_bits if b not in bitmap]
        return {"flags": flags, "unknown_bits": unknown}

    def updateData(self):
        self.readInputRegisters()
        regs = self.result.registers

        decoded = self._decode_by_map(regs)
        self.data.update(decoded)

        # Expand warning/alarm bitfields into flags + unknown bits
        if "warning_state_raw" in self.data:
            d = self._decode_flags(self.data["warning_state_raw"], self.WARNING_BITS)
            self.data["warning_flags"] = d["flags"]
            self.data["warning_unknown_bits"] = d["unknown_bits"]
        if "alarm_state_raw" in self.data:
            d = self._decode_flags(self.data["alarm_state_raw"], self.ALARM_BITS)
            self.data["alarm_flags"] = d["flags"]
            self.data["alarm_unknown_bits"] = d["unknown_bits"]

        # Derived quantities
        lp = self.data.get("low_pressure")
        hp = self.data.get("high_pressure")
        if isinstance(lp, (int, float)) and isinstance(hp, (int, float)):
            self.data["delta_pressure"] = hp - lp

        cin = self.data.get("coolant_in_temp")
        cout = self.data.get("coolant_out_temp")
        if isinstance(cin, (int, float)) and isinstance(cout, (int, float)):
            self.data["coolant_deltaT"] = cout - cin

        return self.data

    # ---- Control (verify addresses/values in your model manual) ----
    def turnOn(self, address=1, value=0x0001):
        return self.client.write_register(address, value, unit=self.unit)

    def turnOff(self, address=1, value=0x00FF):
        return self.client.write_register(address, value, unit=self.unit)


# ----------- CSV Logger (no plotting) -----------------------------------------

DEFAULT_FIELDS = [
    "operating_state", "compressor_running",
    "warning_state_raw", "alarm_state_raw",
    "low_pressure", "low_pressure_avg",
    "high_pressure", "high_pressure_avg",
    "delta_pressure", "delta_pressure_avg",
    "coolant_in_temp", "coolant_out_temp", "coolant_deltaT",
    "oil_temp", "helium_temp",
    "motor_current", "operating_hours",
    # If you add to REGMAP, you can include them here too.
]

def ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def open_csv_for_day(log_dir, basename, fieldnames, daystamp):
    """
    Open daily CSV in binary append mode for Py2 csv module.
    Returns (file_obj, csv_writer, csv_path, wrote_header_now)
    """
    ensure_dir(log_dir)
    csv_path = os.path.join(log_dir, "%s_%s.csv" % (basename, daystamp))
    f = io.open(csv_path, mode="ab")
    writer = csv.DictWriter(f, fieldnames=["timestamp"] + fieldnames)
    wrote_header_now = False
    try:
        if os.path.getsize(csv_path) == 0:
            writer.writeheader()
            wrote_header_now = True
    except Exception:
        writer.writeheader()
        wrote_header_now = True
    return f, writer, csv_path, wrote_header_now

def poll_loop(ip, unit, start, count, period, fields, log_dir, basename,
              warn_dp_diff=None, cool_dt_min=None, stop_evt=None):
    comp = CompressorControl(ip, unit=unit, start=start, count=count, auto_connect=True)

    current_day = datetime.now().strftime("%Y%m%d")
    f, writer, csv_path, _ = open_csv_for_day(log_dir, basename, fields, current_day)
    sys.stderr.write("[logger] Writing to %s\n" % csv_path)

    try:
        while not (stop_evt and stop_evt.is_set()):
            now = datetime.now()
            daystamp = now.strftime("%Y%m%d")
            ts = now.strftime("%Y-%m-%dT%H:%M:%S")

            # Midnight rotation
            if daystamp != current_day:
                try:
                    f.close()
                except Exception:
                    pass
                current_day = daystamp
                f, writer, csv_path, _ = open_csv_for_day(log_dir, basename, fields, current_day)
                sys.stderr.write("[logger] Rotated to %s\n" % csv_path)

            try:
                d = comp.updateData()  # dict
            except Exception as e:
                sys.stderr.write("[logger] Read error: %s\n" % e)
                time.sleep(period)
                continue

            # Row build
            row = {"timestamp": ts}
            for k in fields:
                row[k] = safe_float(d.get(k, ""))

            # Optional, lightweight sanity alerts to stderr (no spammy prints)
            try:
                if warn_dp_diff is not None:
                    dp = d.get("delta_pressure")
                    dp_avg = d.get("delta_pressure_avg")
                    if isinstance(dp, (int, float)) and isinstance(dp_avg, (int, float)):
                        if abs(dp - dp_avg) > float(warn_dp_diff):
                            sys.stderr.write("[warn] delta_pressure diff > %.2f (%.2f vs %.2f)\n" %
                                             (warn_dp_diff, dp, dp_avg))
                if cool_dt_min is not None:
                    cdt = d.get("coolant_deltaT")
                    if isinstance(cdt, (int, float)) and (cdt < float(cool_dt_min)):
                        sys.stderr.write("[warn] coolant_deltaT below %.2f (%.2f)\n" %
                                         (cool_dt_min, cdt))
                # Unknown warning/alarm bits
                wu = d.get("warning_unknown_bits", [])
                au = d.get("alarm_unknown_bits", [])
                if wu:
                    sys.stderr.write("[warn] unknown warning bits set: %s\n" % wu)
                if au:
                    sys.stderr.write("[warn] unknown alarm bits set: %s\n" % au)
            except Exception:
                pass

            # Write CSV
            try:
                writer.writerow(row)
                f.flush()
            except Exception as e:
                sys.stderr.write("[logger] Write error: %s\n" % e)

            time.sleep(period)
    finally:
        try:
            comp.close()
        except Exception:
            pass
        try:
            f.close()
        except Exception:
            pass


# ----------- CLI --------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Cryomech Compressor Combined Logger (Python 2)")
    ap.add_argument("--ip", required=True, help="Compressor IP, e.g., 192.168.0.36")
    ap.add_argument("--unit", type=int, default=16, help="Modbus Unit ID (default: 16)")
    ap.add_argument("--start", type=int, default=0, help="Input register start (default: 0)")
    ap.add_argument("--count", type=int, default=64, help="Register count to read (default: 64)")
    ap.add_argument("--period", type=float, default=1.0, help="Polling period seconds (default: 1.0)")
    ap.add_argument("--logdir", type=str, default="./logs", help="Directory for CSV files")
    ap.add_argument("--basename", type=str, default="compressor_data", help="CSV file basename")
    ap.add_argument("--fields", type=str, default=",".join(DEFAULT_FIELDS),
                    help="Comma-separated fields to log (must exist in data)")
    # Optional simple guards
    ap.add_argument("--warn-dp-diff", type=float, default=None,
                    help="Warn if |delta_pressure - delta_pressure_avg| exceeds this")
    ap.add_argument("--cool-dt-min", type=float, default=None,
                    help="Warn if coolant_deltaT below this threshold (°C)")
    args = ap.parse_args()

    fields = [s.strip() for s in args.fields.split(",") if s.strip()]

    stop_evt = Event()
    t = Thread(target=poll_loop,
               args=(args.ip, args.unit, args.start, args.count, args.period,
                     fields, args.logdir, args.basename, args.warn_dp_diff, args.cool_dt_min, stop_evt))
    t.daemon = True
    t.start()

    try:
        while t.is_alive():
            t.join(0.5)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        stop_evt.set()
        t.join(2.0)


if __name__ == "__main__":
    main()

