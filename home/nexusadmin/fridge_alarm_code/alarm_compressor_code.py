#! /usr/local/soft/pythonenv/env_alarms/bin/python

#valentina.novati@northwestern.edu
# run with ./alarm_compressor_code.py

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


def read_Data(pathname_series):   
  data = pd.read_csv(pathname_series, delimiter = ',', encoding = 'latin', index_col=False)
  return data


def alarm_reset():
  #print('status', setting['alarm'][TYPE][AL]['status'])
  if (setting['alarm'][TYPE][AL]['status']>0):
    setting['alarm'][TYPE][AL]['status']=0
    setting['alarm'][TYPE][AL]['time']=0
    update_json_settings()
    send_message("Cleared: "+setting['alarm'][TYPE][AL]['text'])
  return()


def alarm_minmax(val, minval, maxval):
  if((val>maxval)|(val<minval)):
    alarm_alarm()
  else:
    alarm_reset()
    #print('here')
  return()


def alarm_statuschange(lista):
  if (np.std(lista)>0):
    alarm_alarm()
  else:
    alarm_reset()
  return()


def date2timestamp(lista):
  timestamp=datetime.datetime(lista[0], lista[1], lista[2], lista[3], lista[4], lista[5], 0)
  return(timestamp)

def readtime(date,heures):
  year=2000+int(date.split(' ')[2])
  month=int(date.split(' ')[1])
  day=int(date.split(' ')[0])
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
    setting['alarm'][TYPE][AL]['status']=1 #trigger the alarm
    setting['alarm'][TYPE][AL]['time']=[now.year,now.month, now.day, now.hour, now.minute, now.second]
    update_json_settings()
    send_message(setting['alarm'][TYPE][AL]['text']+tag)
  return()

def send_reminder(reminder_number):
  send_message("Reminder "+str(reminder_number)+": "+setting['alarm'][TYPE][AL]['text']+tag)
  if (reminder_number==3):
    setting['alarm'][TYPE][AL]['status']=0
  else:
    setting['alarm'][TYPE][AL]['status']=setting['alarm'][TYPE][AL]['status']+1
  update_json_settings()
  return()

homepath='/usr/local/soft/slow_monitor_alarms/'

#loading alarm settings
config_file=homepath+'config_compressor_alarm.json'
with open(config_file) as json_file:
  setting=json.load(json_file)

#slack token
token_file=homepath+'token.json'#'token4test.json' #'token.json'
with open(token_file) as json_file:
  token=json.load(json_file)

#tagging people on slack
slack_tag_file=homepath+'slack_config.json'
with open(slack_tag_file) as json_file:
  tag_dict=json.load(json_file)
tag=" "
for person in tag_dict["slack_ID"].keys():
  tag = tag+tag_dict["slack_ID"][person] 


#load cryostat data
pathname='/home/LogData/CompressorData/'
list_of_files=glob.glob(pathname+"*.csv")
latest_file=max(list_of_files, key=os.path.getctime)
data=read_Data(latest_file)


#there is a recorded value each 5 minutes, running this code once each 10 minutes, I want to look at the last 2 values
filelen=len(data)-1


if (setting['status']['ENABLE']=='True'):   

  #time now
  now = datetime.datetime.now()
  #time in data
  heures=data['time'][filelen]
  day=data['date'][filelen]
  data_time=readtime(day, heures)
  
  #alarm active test
  test_alarm_time=date2timestamp([now.year,now.month, now.day,9,5,0])
  if((now.weekday()==0)&((np.abs(now-test_alarm_time)).total_seconds()<300)):
    send_message("Weekly notification: compressor alarms active")



  #check all the alarms in the config file
  for TYPE in setting['alarm']:
    for AL in setting['alarm'][TYPE]:
      namestr=setting['alarm'][TYPE][AL]['name']
      stat=setting['alarm'][TYPE][AL]['status']
      time_last_alarm=setting['alarm'][TYPE][AL]['time']
      data_ar=data[namestr][filelen-2:].tolist()

      #cycle the various alarm type and alarm variables and check the states of alarms
     
      if (TYPE=='minmax_alarm'):
        minval=setting['alarm'][TYPE][AL]['min']
        maxval=setting['alarm'][TYPE][AL]['max']
        if(AL=='time update'):
          #print(now, data_time)
          #print((now-data_time).total_seconds())
          alarm_minmax((now-data_time).total_seconds(), minval,maxval)
        else:
          alarm_minmax(data_ar[2], minval,maxval)

      if (TYPE=='status_alarm'):
        alarm_statuschange(data_ar)


      if (stat>0):
        #send reminders
        time_from_last_alarm=(now-date2timestamp(time_last_alarm)).total_seconds()
        if ((time_from_last_alarm>600)&(stat==1)): #after 10 min
           send_reminder(stat)
           
        if ((time_from_last_alarm>3600)&(stat==2)): #after 1 hour
           send_reminder(stat)

        if ((time_from_last_alarm>28800)&(stat==3)): #after 8 hours
           send_reminder(stat)

