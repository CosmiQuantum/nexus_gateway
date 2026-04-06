#! /bin/bash
#flock -n data_bridge.flag rsync -avzPe ssh /mnt/NexusData/Bridge/* ktk@centos7.slac.stanford.edu:/nfs/slac/g/supercdms/www/nexus/fridge/LakeshoreBridge/. > /dev/null 2>&1
#cmd="flock -n data_bridge.flag rsync -avzPe ssh /mnt/NexusData/Bridge/* ktk@centos7.slac.stanford.edu:/nfs/slac/g/supercdms/www/nexus/fridge/LakeshoreBridge/. > /dev/null 2>&1"
#cmd2="flock -n data_sync_cc.flag rsync -avuzOL --chmod=2750 -P -e ssh /mnt/NexusData/Bridge/* ktk1027@narval.computecanada.ca:/project/def-zqhong/RicochetData/NEXUS/LakeshoreData > cronjob_cc_bridge.log"
cmd="flock -n data_bridge.flag rsync -avzPe ssh /home/LogData/LakeshoreData/* ktk@centos7.slac.stanford.edu:/nfs/slac/g/supercdms/www/nexus/fridge/LakeshoreBridge/. > /dev/null 2>&1"
#cmd2="flock -n data_sync_cc.flag rsync -avuzOL --chmod=2750 -P -e ssh /home/LogData/LakeshoreData/* ktk1027@narval.computecanada.ca:/project/def-zqhong/RicochetData/NEXUS/LakeshoreData > cronjob_cc_bridge.log"
cmd2="flock -n data_sync_cc.flag rsync -avuzOL --chmod=2750 -P -e ssh /home/LogData/LakeshoreData/* ktk1027@robot.narval.alliancecan.ca:/project/def-zqhong/RicochetData/NEXUS/LakeshoreData > cronjob_cc_bridge.log"
eval $cmd
eval $cmd2
