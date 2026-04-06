#! /bin/bash
#flock -n data_macrt_uoft.flag rsync -avzPe ssh /mnt/fridge_log/* tes-lab@tes-uoft.com:/home/tes-lab/nexus_fridge_monitor/fridge/files/. > /dev/null 2>&1
flock -n data_macrt_uoft.flag rsync -avzPe ssh /mnt/fridge_log_old_fridge_computer/* tes-lab@tes-uoft.com:/home/tes-lab/nexus_fridge_monitor/fridge/files/. > /dev/null 2>&1
#flock -n data_plc_uoft.flag rsync -avzPe ssh /mnt/plc_log/* tes-lab@tes-uoft.com:/home/tes-lab/nexus_fridge_monitor/fridge/plcFiles/. > /dev/null 2>&1
flock -n data_plc_uoft.flag rsync -avzPe ssh /mnt/plc_log_old_fridge_computer/* tes-lab@tes-uoft.com:/home/tes-lab/nexus_fridge_monitor/fridge/plcFiles/. > /dev/null 2>&1
flock -n data_compressor_uoft.flag rsync -avzPe ssh /home/LogData/CompressorData/* tes-lab@tes-uoft.com:/home/tes-lab/nexus_fridge_monitor/fridge/compressorFiles/. > /dev/null 2>&1
flock -n data_plc_uoft.flag rsync -avzPe ssh /usr/local/soft/NetDeviceCtrl/LN2_data/* tes-lab@tes-uoft.com:/home/tes-lab/nexus_fridge_monitor/fridge/ln2_files/. > /dev/null 2>&1
