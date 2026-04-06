#! /usr/local/soft/pythonenv/env_alarms/bin/python

#valentina.novati@northwestern.edu
# run with ./alarm_code.py

import pandas as pd
import numpy as np
import json
import datetime
import time
import os
import glob
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def send_message(text_message):
  #client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
  client = WebClient(token=token['token'])


  try:
    response = client.chat_postMessage(channel='#nexus_fridge', text=text_message)
    #"This still works and the fridge is not working today! \n 2 line message")
    #assert response["message"]["text"] == "Hello Tina!"
  except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["ok"] is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print("Got an error: {e.response['error']}")
  return()


def read_plcData(pathname_series):   
  data = pd.read_csv(pathname_series, delimiter = '\t', encoding = 'latin', index_col=False)
  return data


def alarm_reset():
  if (setting[TEMP][TYPE][AL]['status']>0):
    setting[TEMP][TYPE][AL]['status']=0
    setting[TEMP][TYPE][AL]['time']=0
    update_json_settings()
    send_message("Cleared: "+setting[TEMP][TYPE][AL]['text'])
  return()


def alarm_minmax(val, minval, maxval):
  if((val>maxval)|(val<minval)):
    alarm_alarm()
  else:
    alarm_reset()
  return()

# I am printing the values that make trigger the alarm on the log file, this alarm triggers more than I would like...
def alarm_stale(lista):
  if (np.std(lista)<1e-12):
    print(lista, np.std(lista))
    alarm_alarm()
  else:
    alarm_reset()
  return()


def alarm_statuschange(lista):
  if (np.std(lista)>0):
    alarm_alarm()
  else:
    alarm_reset()
  return()


def alarm_comparison(val1, val2, threshold):
  if (np.abs(val1- val2)>threshold):
    alarm_alarm()
  else:
    alarm_reset()
  return()

def alarm_crossing(data_ar, delta, crossing_point):
  #print(data_ar[0], data_ar[5], np.mean(data_ar), np.mean(data_ar)-crossing_point)
  if ((np.abs(np.mean(data_ar)-crossing_point)<delta)&(data_ar[0]>data_ar[5])):
    alarm_alarm()
  else:
    alarm_reset()     
  return()

def date2timestamp(lista):
  timestamp=datetime.datetime(lista[0], lista[1], lista[2], lista[3], lista[4], lista[5], 0)
  return(timestamp)

def readtime(date,heures):
  year=2000+int(date.split('/')[2])
  month=int(date.split('/')[0])
  day=int(date.split('/')[1])
  hour=int(heures.split(':')[0])
  minute=int(heures.split(':')[1])
  second=int(heures.split(':')[2])
  data_time=date2timestamp([year,month,day,hour,minute,second])
  return(data_time)

def update_json_settings():
  with open(config_file, "w") as outfile:
    json.dump(setting, outfile, indent=4)
  return()


def alarm_alarm():
  if (stat==0): #check that the alarm isn't already triggered
    setting[TEMP][TYPE][AL]['status']=1 #trigger the alarm
    setting[TEMP][TYPE][AL]['time']=[now.year,now.month, now.day, now.hour, now.minute, now.second]
    update_json_settings()
    send_message(setting[TEMP][TYPE][AL]['text']+tag)
  return()

def send_reminder(reminder_number):
  send_message("Reminder "+str(reminder_number)+": "+setting[TEMP][TYPE][AL]['text']+tag)
  if (reminder_number==3):
    setting[TEMP][TYPE][AL]['status']=0
  else:
    setting[TEMP][TYPE][AL]['status']=setting[TEMP][TYPE][AL]['status']+1
  update_json_settings()
  return()

homepath='/usr/local/soft/slow_monitor_alarms/'


#loading alarm settings
config_file=homepath+'config_alarm.json'
with open(config_file) as json_file:
  setting=json.load(json_file)

#slack token
token_file=homepath+'token.json'#'token4test.json' #'token.json'
with open(token_file) as json_file:
  token=json.load(json_file)
#print(token['token'])

#tagging people on slack
slack_tag_file=homepath+'slack_config.json'
with open(slack_tag_file) as json_file:
  tag_dict=json.load(json_file)
tag=" "
for person in tag_dict["slack_ID"].keys():
  tag = tag+tag_dict["slack_ID"][person] 


#load cryostat data
#pathname='/mnt/plc_log/'
pathname='/mnt/plc_log_old_fridge_computer/'
#list_of_files=glob.glob(pathname+"*.txt")
#latest_file=max(list_of_files, key=os.path.getctime)
#data=read_plcData(latest_file)
try:
    list_of_files = glob.glob(os.path.join(pathname, "*.txt"))
    if not list_of_files:  # glob worked, but no files found
        send_message(f"No files found in {pathname}, likely Fridge computer crashed {tag}")
    else:
        latest_file = max(list_of_files, key=os.path.getctime)
        data = read_plcData(latest_file)
except OSError as e:
    # This will catch "Host is down" or other I/O errors
    send_message(f"{pathname} not accessible: {e} {tag}")

#data=read_plcData(homepath+'211108.txt')

#there is a recorded value each 10 sec, running this code once a minute, I want to look at the last 6 values
filelen=len(data)-1

#send_message('Hello!')

if (setting['status']['ENABLE']=='True'):   

  #time now
  now = datetime.datetime.now()
  #time in data
  heures=data['heures'][filelen]
  day=data['date'][filelen]
  data_time=readtime(day, heures)
  
  #alarm active test
  test_alarm_time=date2timestamp([now.year,now.month, now.day,9,0,0])
  if((now.weekday()==1)&((np.abs(now-test_alarm_time)).total_seconds()<30)):
    send_message("Weekly notification: "+ setting['status']['fridge_temp'] +" active")

  #cold or warm alarm set in the config file 
  TEMP=setting['status']['fridge_temp']

  #check all the alarms in the config file
  for TYPE in setting[TEMP]:
    for AL in setting[TEMP][TYPE]:
      namestr=setting[TEMP][TYPE][AL]['name']
      stat=setting[TEMP][TYPE][AL]['status']
      time_last_alarm=setting[TEMP][TYPE][AL]['time']
      data_ar=data[namestr][filelen-5:].tolist()
      data_ar_stale=data[namestr][filelen-120:].tolist() 

      #cycle the various alarm type and alarm variables and check the states of alarms
      #if (stat==0):
      if (TYPE=='minmax_alarm'):
        minval=setting[TEMP][TYPE][AL]['min']
        maxval=setting[TEMP][TYPE][AL]['max']
        #print(AL)
        if(AL=='time update'):
          alarm_minmax((now-data_time).total_seconds(), minval,maxval)
        else:
          alarm_minmax(np.mean(data_ar), minval,maxval)

      if ((TYPE=='alarm_stale')&(len(data_ar_stale)>90)):
        alarm_stale(data_ar_stale)

      if (TYPE=='status_alarm'):
        alarm_statuschange(data_ar)

      if (TYPE=='comparison_alarm'):
        namestr2=setting[TEMP][TYPE][AL]['name2']
        threshold=setting[TEMP][TYPE][AL]['threshold']

        data_ar2=data[namestr2][filelen-6:].tolist()
        alarm_comparison(np.mean(data_ar), np.mean(data_ar2), threshold)

      if (TYPE=='crossing_alarm'):
        crossing_point=setting[TEMP][TYPE][AL]['cross']
        delta=setting[TEMP][TYPE][AL]['delta']
        alarm_crossing(data_ar, delta, crossing_point)
            
      if (stat>0):
        #send reminders
        time_from_last_alarm=(now-date2timestamp(time_last_alarm)).total_seconds()
        if ((time_from_last_alarm>600)&(stat==1)): #after 10 min
           send_reminder(stat)
           
        if ((time_from_last_alarm>3600)&(stat==2)): #after 1 hour
           send_reminder(stat)

        if ((time_from_last_alarm>28800)&(stat==3)): #after 8 hours
           send_reminder(stat)

