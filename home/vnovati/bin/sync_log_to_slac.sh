#! /bin/bash
flock -n data_macrt.flag rsync -avzPe ssh /mnt/fridge_log/* vnovati@centos7.slac.stanford.edu:/nfs/slac/g/supercdms/www/nexus/fridge/files/. > /dev/null 2>&1
flock -n data_plc.flag rsync -avzPe ssh /mnt/plc_log/* vnovati@centos7.slac.stanford.edu:/nfs/slac/g/supercdms/www/nexus/fridge/plcFiles/. > /dev/null 2>&1
flock -n data_compressor.flag rsync -avzPe ssh /home/LogData/CompressorData/* vnovati@centos7.slac.stanford.edu:/nfs/slac/g/supercdms/www/nexus/fridge/compressorFiles/. > /dev/null 2>&1
