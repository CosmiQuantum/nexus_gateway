#! /usr/local/soft/pythonenv/env_alarms/bin/python

# valentina.novati@northwestern.edu
# run with ./alarm_reset.py

import json

#alarm settings files
config_file='config_compressor_alarm.json'

with open(config_file) as json_file:
  setting=json.load(json_file)

for TYPE in setting['alarm']:
  print(TYPE)
  for AL in setting['alarm'][TYPE]:
    setting['alarm'][TYPE][AL]['status']=0
    setting['alarm'][TYPE][AL]['time']=0
  

with open(config_file, "w") as outfile:
  json.dump(setting, outfile, indent=4)


