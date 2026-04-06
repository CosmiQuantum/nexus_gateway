#! /bin/bash
#flock -n data_bridge.flag rsync -avzPe ssh /mnt/NexusData/Bridge/* vnovati@centos7.slac.stanford.edu:/nfs/slac/g/supercdms/www/nexus/fridge/LakeshoreBridge/. > /dev/null 2>&1
cmd="flock -n data_bridge.flag rsync -avzPe ssh /mnt/NexusData/Bridge/* vnovati@centos7.slac.stanford.edu:/nfs/slac/g/supercdms/www/nexus/fridge/LakeshoreBridge/. > /dev/null 2>&1"
cmd2="flock -n data_sync_cc.flag rsync -avuzOL --chmod=2750 -P -e ssh /mnt/NexusData/Bridge/* vnovati@narval.computecanada.ca:/project/def-zqhong/RicochetData/NEXUS/LakeshoreData > cronjob_cc_bridge.log"
eval $cmd
eval $cmd2
