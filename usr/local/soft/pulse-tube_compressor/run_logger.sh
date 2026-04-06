#! /bin/bash

#environment source from nexus-network
#source /home/nexusadmin/miniconda2/etc/profile.d/conda.sh
#conda activate PTComp

#environment source that should work on nexus-gateway -- needs to be tested
source /usr/local/soft/pythonenv/env_compressor/venv_compressor/bin/activate

python /usr/local/soft/pulse-tube_compressor/compressorLogger.py

