#! /bin/bash
#flock -n data_macrt.flag rsync -avzPe ssh /mnt/fridge_log/* nraha@colossus.northwestern.edu:/var/www/Nexsus_fridge.com/Nexus_fridge/fridge/files/. > /dev/null 2>&1
flock -n data_macrt.flag rsync -avzPe ssh /mnt/fridge_log_old_fridge_computer/* nraha@colossus.northwestern.edu:/var/www/Nexsus_fridge.com/Nexus_fridge/fridge/files/. > /dev/null 2>&1
#flock -n data_plc.flag rsync -avzPe ssh /mnt/plc_log/* nraha@colossus.northwestern.edu:/var/www/Nexsus_fridge.com/Nexus_fridge/fridge/plcFiles/. > /dev/null 2>&1
flock -n data_plc.flag rsync -avzPe ssh /mnt/plc_log_old_fridge_computer/* nraha@colossus.northwestern.edu:/var/www/Nexsus_fridge.com/Nexus_fridge/fridge/plcFiles/. > /dev/null 2>&1
flock -n data_compressor.flag rsync -avzPe ssh /home/LogData/CompressorData/* nraha@colossus.northwestern.edu:/var/www/Nexsus_fridge.com/Nexus_fridge/fridge/compressorFiles/. > /dev\
/null
flock -n data_plc.flag rsync -avzPe ssh /usr/local/soft/NetDeviceCtrl/LN2_data/* nraha@colossus.northwestern.edu:/var/www/Nexsus_fridge.com/Nexus_fridge/fridge/ln2_files/. > /dev/null 2>&1
