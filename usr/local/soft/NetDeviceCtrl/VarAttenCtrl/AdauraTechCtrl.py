import sys
from time import sleep

try:
    from NetDrivers import VarAtten
except ImportError:
    try:
        sys.path.append('/usr/local/src/NetDeviceCtrl/NetDrivers')
        from VarAtten import VarAtten
    except ImportError:
        print("Cannot find the VarAtten driver")
        exit()

atten = VarAtten("192.168.0.230") #Do I need to add a server port here?

#----------------------------------------------------------
#------------------ RUN 1 SPECIFIC CODE -------------------
#----------------------------------------------------------

# Some of this code is going to be behind "passwords" so that it's not easily callable
# without a little bit of additional forethought

# Set attenuators to a high-attenuation state
def SetAttenuatorsToSafeState():
    vals = [95,95,95,95,95,95,95,95]
    atten.SetAllChannels(vals);

# Open up the VNA channel (low-attenuation)
def SetVNAChannelsToOpenState():
    atten.SetChannel(7,0,verbose=True)
    atten.SetChannel(8,0,verbose=True)

# Set the VNA channels to a safe (high-attenuation) state
def SetVNAChannelsToSafeState():
    atten.SetChannel(7,95,verbose=True)
    atten.SetChannel(8,95,verbose=True)
    
# Set the Silicon Chip's Qubit post-DAC attenuation
def SetSiliconChipQubitAttenuation(val):
    atten.SetChannel(6,val,verbose=True)

# Set the Silicon Chip's Resonator post-DAC attenuation
def SetSiliconChipResonatorAttenuation(val):
    atten.SetChannel(4,val,verbose=True)

# Set the Sapphire Chip's Qubit post-DAC attenuation
def SetSapphireChipQubitAttenuation(val):
    atten.SetChannel(5,val,verbose=True)

# Set the Sapphire Chip's Resonator post-DAC attenuation
def SetSapphireChipResonatorAttenuation(val):
    atten.SetChannel(3,val,verbose=True)

# Set the Sapphire Chip's Resonator post-DAC attenuation
def SetKIDChipAttenuation(val):
    atten.SetChannel(2,val,verbose=True)

# Initialize attenuators to a VNA test state
def InitializeAttenuatorsForVNATests_Run1():
    SetAttenuatorsToSafeState()
    SetVNAChannelsToOpenState()
    SetSiliconChipQubitAttenuation(95)
    SetSiliconChipResonatorAttenuation(95)
    SetSapphireChipQubitAttenuation(95)
    SetSapphireChipResonatorAttenuation(95)
    SetKIDChipAttenuation(95)

# Initialize attenuators for a sapphire-only run. Kills all channels that are not from
# the sapphire qubit or resonator.
def InitializeAttenuatorsForSapphireQubitTests_Run1(saph_qubit_att,saph_res_att):
    SetAttenuatorsToSafeState()
    SetVNAChannelsToSafeState()
    SetSiliconChipQubitAttenuation(95)
    SetSiliconChipResonatorAttenuation(95)
    SetSapphireChipQubitAttenuation(saph_qubit_att)
    SetSapphireChipResonatorAttenuation(saph_res_att)
    SetKIDChipAttenuation(95)

# Initialize attenuators for a sapphire-only run. Kills all channels that are not from
# the sapphire qubit or resonator.
def InitializeAttenuatorsForSiliconQubitTests_Run1(sil_qubit_att,sil_res_att):
    SetAttenuatorsToSafeState()
    SetVNAChannelsToSafeState()
    SetSiliconChipQubitAttenuation(sil_qubit_att)
    SetSiliconChipResonatorAttenuation(sil_res_att)
    SetSapphireChipQubitAttenuation(95)
    SetSapphireChipResonatorAttenuation(95)
    SetKIDChipAttenuation(95)

# Initialize attenuators for a sapphire-only run. Kills all channels that are not from
# the sapphire qubit or resonator.
def InitializeAttenuatorsForKIDTests_Run1(kid_att):
    SetAttenuatorsToSafeState()
    SetVNAChannelsToSafeState()
    SetSiliconChipQubitAttenuation(95)
    SetSiliconChipResonatorAttenuation(95)
    SetSapphireChipQubitAttenuation(95)
    SetSapphireChipResonatorAttenuation(95)
    SetKIDChipAttenuation(kid_att)

    
    
#------------------ Debugging code -------------------------




# Function that sets a given channel. We don't want this generally accessible,
# so it's going to hide behind an (easily-findable) password
def SetChannel(ch,att,password):
    if password == "PleaseAndThankYou":
        atten.SetChannel(ch,att,verbose=True)
    else:
        print("Incorrect password for arbitrary attenuator channel setting. Request denied. It is recommended you use the dedicated functions for collective channel setting.")


# Do a check to see what the values of the different channels are
def AttenuatorRollCall():
    atten.GetChannelStatus(verbose=True)

def GetDeviceInfoTest():
    print(atten.GetDeviceInfo())

    

def Reset():
    atten.Reset(verbose=True)



if __name__ == "__main__":
    RollCall()
