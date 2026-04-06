#!/usr/bin/env python2
#need to use python2 because the pymodbus package isn't supported on 3
# -*- coding: utf-8 -*-

#import the stuff we made
from CompressorControl import CompressorControl

#TODO: change it so that this accepts the IP address as an input parameter and pass it through arguments
def main():
    #set up communication with the compressor
 #   comp = CompressorControl('169.254.195.21')
    comp = CompressorControl('192.168.0.36')
    #turn on the compressor
    comp.turnOff()

if __name__=="__main__":
    main()
