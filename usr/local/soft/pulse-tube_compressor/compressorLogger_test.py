#!/usr/bin/env python2
#need python2 because the pymodbus package isn't supported on 3
# -*- coding: utf-8 -*-
#python standard stuff
from datetime import datetime

#import the stuff we made
from DataLogger import DataLogger
from CompressorControl_pratyush import CompressorControl 
#from CompressorControl import CompressorControl

#TODO: change it so that this accepts the IP address as an input parameter and pass it through arguments
#set up communication with the compressor
comp = CompressorControl('192.168.0.36')
#get the data
comp.updateData()
data = comp.data
print(data)
