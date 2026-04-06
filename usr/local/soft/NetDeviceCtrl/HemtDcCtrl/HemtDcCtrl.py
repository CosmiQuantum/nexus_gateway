import sys
from time import sleep

try:
    from NetDrivers import E36300
except ImportError:
    try:
        sys.path.append('../NetDrivers')
        from E36300 import E36300
    except ImportError:
        print("Cannot find the E36300 driver")
        exit()

hemts = [ E36300("192.168.0.201",server_port=5025) ,  ## Chet
          E36300("192.168.0.202",server_port=5025) ]  ## Carlos

def RollCall():

    for i in range(len(hemts)):
        print("HEMT "+str(i+1))
        hemt = hemts[i]
        print(hemt.getID())
        print(hemt.getVoltage())
        print(hemt.getCurrent())
        print(hemt.getStatus())
        print("")

def HEMTsOn():

    for i in range(len(hemts)):
        print("HEMT "+str(i+1))
        hemt = hemts[i]
        print("Status")
        print(hemt.getStatus())
        print("Enabling")
        hemt.enable([2,3])
        sleep(1)
        print("New Status")
        print(hemt.getVoltage())
        print(hemt.getCurrent())
        print(hemt.getStatus())
        print("")

def HEMTsOff():
    for i in range(len(hemts)):
        print("HEMT "+str(i+1))
        hemt = hemts[i]
        print("Status")
        print(hemt.getStatus())
        print("Disabling")
        hemt.disable([2,3])
        sleep(1)
        print("New Status")
        print(hemt.getVoltage())
        print(hemt.getCurrent())
        print(hemt.getStatus())
        print("")

if __name__ == "__main__":
    RollCall()