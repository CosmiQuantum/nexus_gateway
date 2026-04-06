#! /bin/bash

#environment source from nexus-network
#source /home/nexusadmin/miniconda2/etc/profile.d/conda.sh
#conda activate PTComp

#environment source that should work on nexus-gateway -- needs to be tested
source /usr/local/soft/pythonenv/env_compressor/venv_compressor/bin/activate

python /usr/local/soft/pulse-tube_compressor/compressorLogger_test.py

#python /usr/local/soft/pulse-tube_compressor/compressorLogger_test_continious.py \
#  --ip 192.168.0.36 \
#  --period 1 \
#  --logdir /usr/local/soft/pulse-tube_compressor \
#  --basename compressor_data
