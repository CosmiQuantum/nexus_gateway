"""
NetDrivers (NetDeviceCtrl).

Drivers and interfaces for using lab equipment over a network
"""

__version__ = "1.0.0"
__author__  = 'Dylan J Temples'
__credits__ = 'Fermi National Accelerator Laboratory'

try:
	## Import every class from each driver file
	from .NetDevice import *
	from .AFG3102   import *
	from .E3631A    import *
	from .E36300    import *
	from .RFSwitch  import *
	from .VarAtten  import *

except ImportError as err:
    print("\033[1;31mERROR\033[0m: Import error from NetDrivers lib.")
    print(err)