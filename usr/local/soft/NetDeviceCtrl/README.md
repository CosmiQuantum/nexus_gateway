# NetDeviceCtrl
Software to interface with network-controllable devices and instrumentation

## Installation via `pip`
After cloning this directory, use the following commands to install this module such that the drivers can be used in code elsewhere on the machine.
```
$ cd NetDeviceCtrl
$ pip install .
```
Be sure to activate an environment first if you wish to.

Once that is complete, in any script where you want to use the drivers, simply add the following line to the top of your python file.
```
from NetDrivers import <CLASS>
```
where `<CLASS>` is one of the following:
- `AFG3102`
- `E3631A`
- `E36300`
- `RFSwitch`
- `VarAtten`

You may also import `NetDevice` if you wish to build your own driver using this backend.

#### NetDrivers
This directory contains the base classes (inside `NetDevice.py`) from which all specific instrument drivers inherit, as well as the specific instrument driver classes. If you are writing a piece of control software using these drivers, it should live in its own directory. The following instruments have drivers written:
- Tektronix Arbitrary Waveform Generator AFG3102 (`AFG3102.py`)
- HP Programmable DC Power Supply E3631A (`E3631A.py`)
- Keysight Programmable DC Power Supply E36312A (`E36300.py`)
- Minicircuits ZTRC-4SPDT-A18 RF Switch  (`RFSwitch.py`)
- AduaraTech 8-channel variable RF attenuator (`VarAtten.py`)

### Using the application-specific code

If you wish to use higher-level methods that are typically application/facility-specific, you may do so by adding the the following line(s) to the top of your script.
```
import VarAttenCtrl as varatt
import HemtDcCtrl as hemt
```

#### RFSwitchCtrl
This directory contains the control software interface for the MiniCircuits RF switch.

#### HemtDcCtrl
This directory contains the control software interface for the Keysight DC power supplies that bias the HEMT amplifiers.

#### VarAttenCtrl
This directory contains the control software interface for the AduaraTech variable RF attenuator.