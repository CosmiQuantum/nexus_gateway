#! /bin/bash
#flock -n data_macrt.flag 
#rsync -avzPe ssh /mnt/fridge_log/* rgualtie@colossus.northwestern.edu:/var/www/Nexsus_fridge.com/Nexus_fridge/fridge/files/. > /dev/null 2>&1 
flock -n data_macrt.flag rsync -avzPe ssh /mnt/fridge_log_old_fridge_computer/* rgualtie@colossus.northwestern.edu:/var/www/Nexsus_fridge.com/Nexus_fridge/fridge/files/. > /dev/null 2>&1
#flock -n data_plc.flag 
#rsync -avzPe ssh /mnt/plc_log/* rgualtie@colossus.northwestern.edu:/var/www/Nexsus_fridge.com/Nexus_fridge/fridge/plcFiles/. > /dev/null 2>&1 
flock -n data_plc.flag rsync -avzPe ssh /mnt/plc_log_old_fridge_computer/* rgualtie@colossus.northwestern.edu:/var/www/Nexsus_fridge.com/Nexus_fridge/fridge/plcFiles/. > /dev/null 2>&1
#flock -n data_compressor.flag 
flock -n data_compressor.flag rsync -avzPe ssh /home/LogData/CompressorData/* rgualtie@colossus.northwestern.edu:/var/www/Nexsus_fridge.com/Nexus_fridge/fridge/compressorFiles/. > /dev/null 2>&1
