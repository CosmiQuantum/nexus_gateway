#! /usr/bin/env python3
from pymodbus.client.sync import ModbusTcpClient
import struct

def arrangeBytes(b1, b2):
    return struct.unpack('>f',struct.pack('>HH',b1,b2))[0]
class CompressorControl:
    def __init__(self, addr):
        self.IP = addr #set the IP address
        self.client = ModbusTcpClient(self.IP) #create the
        self.result = None #initialize somewhere to put the result
        self.data = {} #somewhere for the data
    def readInputRegisters(self):
        self.result = self.client.read_input_registers(0, 35, unit=16) #update the input registers
    def updateData(self):
        self.readInputRegisters() #read the input registers
        arr = self.result.registers #get the registers in an array
        #put the keys in a dictionary
        self.data['operating_state']= arr[0]
        self.data['compressor_running']= arr[1]
        self.data['warning_state']= arrangeBytes(arr[4],arr[3])
        self.data['alarm_state']= arrangeBytes(arr[6],arr[5])
        self.data['coolant_in_temp']= arrangeBytes(arr[8],arr[7])
        self.data['coolant_out_temp']= arrangeBytes(arr[10],arr[9])
        self.data['oil_temp']= arrangeBytes(arr[12],arr[11])
        self.data['helium_temp']= arrangeBytes(arr[14],arr[13])
        self.data['low_pressure']= arrangeBytes(arr[16],arr[15])
        self.data['low_pressure_avg']= arrangeBytes(arr[18],arr[17])
        self.data['high_pressure']= arrangeBytes(arr[20],arr[19])
        self.data['high_pressure_avg']= arrangeBytes(arr[22],arr[21])
        self.data['delta_pressure_avg']= arrangeBytes(arr[24],arr[23])
        self.data['motor_current']= arrangeBytes(arr[26],arr[25])
        self.data['operating_hours']= arrangeBytes(arr[28],arr[27])

    def turnOn(self):
    #turn the compressor on
        self.client.write_register(1, int("0x0001", 16))
    def turnOff(self):
    #turn the compressor off
        self.client.write_register(1, int("0x00FF", 16))

    def __del__(self):
        #close the TCP connection when the object gets destroyed
        self.client.close()

