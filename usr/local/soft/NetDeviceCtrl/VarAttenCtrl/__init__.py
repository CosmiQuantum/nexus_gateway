"""
VarAttenCtrl (NetDeviceCtrl).

High-level application/facility-specific functions of the Variable Attenuator
"""

__version__ = "1.0.0"
__author__  = 'Dylan J Temples'
__credits__ = 'Fermi National Accelerator Laboratory'

try:
	from .AdauraTechCtrl import *

except ImportError as err:
    print("\033[1;31mERROR\033[0m: Import error from VarAttenCtrl lib.")
    print(err)