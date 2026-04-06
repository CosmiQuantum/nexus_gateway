#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import traceback
#import sys
import os
import time
#import asyncio
import csv
import datetime
#import subprocess
import math

today_date = datetime.date.today()

from datetime import datetime, timedelta
from NetDrivers import NetDevice

# Define the file name for the CSV
csv_filename = "/usr/local/soft/NetDeviceCtrl/LN2_data/" +str(today_date) + "_LN2_level.csv"

ln = NetDevice(server_ip="192.168.0.201",server_port=7180)
#ln._sendCmd("MEASure:N2:LEVel?",getResponse=True,verbose=False)
#ln2_level = ln._sendCmd("FILL:B?")
#ln2_time = ln._sendCmd("SYStem:TIME?")

start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
end_time = start_time + timedelta(hours=24)

headernames=['Timestamp', 'Time', 'LN2 - level (%)']

if not os.path.exists(csv_filename):
    with open(csv_filename, "w", newline='') as csv_file:
        # Header of the CSV:
        writer = csv.DictWriter(csv_file,fieldnames=headernames)
        writer.writeheader()

with open(csv_filename, "a", newline='') as csv_file:
    # Header of the CSV:
    # headernames=['Timestamp', 'Time', 'LN2 - level (%)']
    writer = csv.DictWriter(csv_file,fieldnames=headernames)    
    # writer.writeheader()
    #print(csv_filename)
    #end_of_day = datetime.now() + timedelta(hours=24)
    #end_time = end_of_day - datetime.now()
    # Data in a file for a day
    while datetime.now() < end_time:
        time.sleep(10)
        # Convert it to a Unix timestamp
        try:
            ln2_level = ln._sendCmd("MEASure:N2:LEVel?",getResponse=True,verbose=False)
        except ConnectionResetError as e:
            print("Error:",e)
            continue;
        ln2_level_str = ln2_level[0]
        try:
            ln2_level_int = float(ln2_level_str)
            #print("Good reading:", ln2_level_int)
        except ValueError as e:
            print("Bad reading:",ln2_level_str)
            continue;
        if math.isnan(ln2_level_int) or ln2_level_int<0.0 or ln2_level_int>150.0:
            continue;
        time_now = datetime.now()
        current_time = time_now.time()
        unix_timestamp = time_now.timestamp() # Convert it to a Unix timestamp
        writer.writerow({'Timestamp':str(unix_timestamp),'Time': current_time.strftime("%H:%M:%S"), 'LN2 - level (%)': str(ln2_level_str)})
        csv_file.flush()
        #print(str(unix_timestamp),current_time.strftime("%H:%M:%S"),str(ln2_level_str))
	#time.sleep(10)

#print("Time = ",ln._sendCmd("SYStem:TIME?"))
