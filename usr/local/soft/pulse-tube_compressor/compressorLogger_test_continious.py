#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse
import csv
import io
import os
import sys
import time
from datetime import datetime
from threading import Event, Thread

# --- your module (must be on PYTHONPATH) ---
from CompressorControl import CompressorControl

DEFAULT_FIELDS = [
    "high_pressure", "low_pressure", "delta_pressure_avg",
    "motor_current", "oil_temp", "coolant_in_temp", "coolant_out_temp",
    "helium_temp", "operating_state", "compressor_running",
    "alarm_state", "warning_state", "operating_hours",
    "low_pressure_avg", "high_pressure_avg"
]

def safe_float(v):
    try:
        return float(v)
    except Exception:
        return v  # if it's not numeric, let csv write the raw

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
    # Binary mode to avoid extra blank lines in Py2
    f = io.open(csv_path, mode="ab")
    writer = csv.DictWriter(f, fieldnames=["timestamp"] + fieldnames)
    wrote_header_now = False
    try:
        if os.path.getsize(csv_path) == 0:
            writer.writeheader()
            wrote_header_now = True
    except Exception:
        # If stat fails, write header once
        writer.writeheader()
        wrote_header_now = True
    return f, writer, csv_path, wrote_header_now

def poll_loop(ip, period, fields, log_dir, basename, stop_evt):
    comp = CompressorControl(ip)

    # initialize day file
    current_day = datetime.now().strftime("%Y%m%d")
    f, writer, csv_path, _ = open_csv_for_day(log_dir, basename, fields, current_day)
    sys.stderr.write("[logger] Writing to %s\n" % csv_path)

    try:
        while not stop_evt.is_set():
            now = datetime.now()
            daystamp = now.strftime("%Y%m%d")
            ts = now.strftime("%Y-%m-%dT%H:%M:%S")

            # rotate file on day change
            if daystamp != current_day:
                try:
                    f.close()
                except Exception:
                    pass
                current_day = daystamp
                f, writer, csv_path, _ = open_csv_for_day(log_dir, basename, fields, current_day)
                sys.stderr.write("[logger] Rotated to %s\n" % csv_path)

            try:
                comp.updateData()
                d = dict(comp.data)  # shallow copy
            except Exception as e:
                sys.stderr.write("[logger] Read error: %s\n" % e)
                time.sleep(period)
                continue

            # build row with selected fields
            row = {"timestamp": ts}
            for k in fields:
                v = d.get(k, "")
                # Best-effort convert numerics; leave text as is
                row[k] = safe_float(v)

            try:
                writer.writerow(row)
                f.flush()
            except Exception as e:
                sys.stderr.write("[logger] Write error: %s\n" % e)

            time.sleep(period)
    finally:
        try:
            f.close()
        except Exception:
            pass

def main():
    ap = argparse.ArgumentParser(description="Python 2 continuous compressor logger (CSV only)")
    ap.add_argument("--ip", required=True, help="Compressor IP (e.g., 192.168.0.36)")
    ap.add_argument("--period", type=float, default=1.0, help="Polling period in seconds (default: 1)")
    ap.add_argument("--fields", type=str, default=",".join(DEFAULT_FIELDS),
                    help="Comma-separated fields to log")
    ap.add_argument("--logdir", type=str, default="./logs",
                    help="Directory to store CSV files (default: ./logs)")
    ap.add_argument("--basename", type=str, default="compressor",
                    help="CSV file basename (default: compressor)")
    args = ap.parse_args()

    fields = [f.strip() for f in args.fields.split(",") if f.strip()]

    stop_evt = Event()
    t = Thread(target=poll_loop, args=(args.ip, args.period, fields, args.logdir, args.basename, stop_evt))
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
