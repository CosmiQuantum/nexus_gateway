This code is reading the output file from the NEXUS fridge.
The code makes some checks on a sub-set of the fridge parameters, if the checks fail a message is sent on slack to a channel.

There are two functioning mode that can be set in the config file _config_alarm.json_:
- the fridge is warm;
- the fridge is cold.

In the first mode (warm), the following checks are done:
- state (open/close) of valve 1;
- log file update (the time difference between the log file and the computer time is < 5 minutes);
- the mixing chamber temperature number is updating.
- pulse tube change of status
- start condensing (mixing chamber temperature < 4.5 K)

In the second mode (cold), the following checks are added to the previous list:
- injection pressure < 800 mbar (pressures K4, K5);
- outlet pressure < 1 mbar (pressure P1);
- mixing chamber temperature < 200 mK;
- differential pressure at the trap is < 10 mbar.
- pulse tube change of status

The code _alarm_code.py_ is launched each minute with a cronjob by nexusadmin.
Once one or more check fail, the alarm is triggered and a message is sent on slack.
The alarm keeps to be triggered and 3 reminders are sent: (1) after 10 minutes; (2) after 1 hour; (3) after 8 hours.
If the alarm is not solved yet, the alarm is de-triggered and it will be re-triggered once the code will be called again, launching a new set of alarms.
The alarms should reset automatically once the parameters go back in the normal range of operations. The code _alarm_reset.py_ can be used to reset manually the alarms.

In addition, a message is sent once a week to confirm that the alarms are activated.

The slack messages can tag the list of people included in the file _slack_config.json_.
