#!/usr/bin/env python2
#need python2 because the pymodbus package isn't supported on 3
# -*- coding: utf-8 -*-
#python standard stuff
from datetime import datetime

#import the stuff we made
from DataLogger import DataLogger
from CompressorControl import CompressorControl

#TODO: change it so that this accepts the IP address as an input parameter and pass it through arguments
def main():
    #set up communication with the compressor
    comp = CompressorControl('192.168.0.36')
    #get the data
    comp.updateData()
    data = comp.data

    #get datetime object for now
    now = datetime.now()
    #make a filename with today's date
    today = datetime.now().strftime("%y%m%d")
    filename = "/home/LogData/CompressorData/Compressor_"+today+".csv"
    #format the date and time strings for the file
    date = now.strftime("%d %m %y")
    time = now.strftime("%H:%M:%S")
    #put it in our dictionary
    data["date"] = date
    data["time"] = time

    headers = [ 'date',
                'time',
                'operating_state',
                'compressor_running',
                'warning_state',
                'alarm_state',
                'coolant_in_temp',
                'coolant_out_temp',
                'oil_temp',
                'helium_temp',
                'low_pressure',
                'low_pressure_avg',
                'high_pressure',
                'high_pressure_avg',
                'delta_pressure_avg',
                'motor_current',
                'operating_hours']

    #make the data logger object
    dl = DataLogger(filename, headers)
    dl.write(data) #finally write the data


if __name__=="__main__":
    main()

