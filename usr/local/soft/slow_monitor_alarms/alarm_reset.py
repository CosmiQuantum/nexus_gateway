#! /usr/local/soft/pythonenv/env_alarms/bin/python

# valentina.novati@northwestern.edu
# run with ./alarm_reset.py

import json

#alarm settings files
config_file='config_alarm.json'

with open(config_file) as json_file:
  setting=json.load(json_file)

for TEMP in ['alarm_cold', 'alarm_warm']:
  for TYPE in setting[TEMP]:
    for AL in setting[TEMP][TYPE]:
      setting[TEMP][TYPE][AL]['status']=0
      setting[TEMP][TYPE][AL]['time']=0
  

with open(config_file, "w") as outfile:
  json.dump(setting, outfile, indent=4)


