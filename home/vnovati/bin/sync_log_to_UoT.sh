#! /bin/bash
flock -n data_macrt.flag rsync -avzPe ssh /mnt/fridge_log/* tes-lab@tes-uoft.com:/home/tes-lab/nexus_fridge_monitor/fridge/files/. > /dev/null 2>&1
flock -n data_plc.flag rsync -avzPe ssh /mnt/plc_log/* tes-lab@tes-uoft.com:/home/tes-lab/nexus_fridge_monitor/fridge/plcFiles/. > /dev/null 2>&1
flock -n data_compressor.flag rsync -avzPe ssh /home/LogData/CompressorData/* tes-lab@tes-uoft.com:/home/tes-lab/nexus_fridge_monitor/fridge/compressorFiles/. > /dev/null 2>&1
