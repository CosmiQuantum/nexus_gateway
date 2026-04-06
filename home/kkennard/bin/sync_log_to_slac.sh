#! /bin/bash
flock -n data_macrt.flag rsync -avzPe ssh /mnt/fridge_log/* ktk@centos7.slac.stanford.edu:/nfs/slac/g/supercdms/www/nexus/fridge/files/. > /dev/null 2>&1
flock -n data_plc.flag rsync -avzPe ssh /mnt/plc_log/* ktk@centos7.slac.stanford.edu:/nfs/slac/g/supercdms/www/nexus/fridge/plcFiles/. > /dev/null 2>&1
flock -n data_compressor.flag rsync -avzPe ssh /home/LogData/CompressorData/* ktk@centos7.slac.stanford.edu:/nfs/slac/g/supercdms/www/nexus/fridge/compressorFiles/. > /dev/null 2>&1
flock -n data_macrt.flag rsync -avzPe ssh /mnt/fridge_log/* ktk1027@robot.narval.alliancecan.ca:/project/def-zqhong/RicochetData/NEXUS/fridge_log/. > /dev/null 2>&1

#flock -n data_macrt.flag rsync -avzPe ssh /mnt/fridge_log/* ktk1027@narval.computecanada.ca:/project/def-zqhong/RicochetData/NEXUS/fridge_log/. > /dev/null 2>&1
