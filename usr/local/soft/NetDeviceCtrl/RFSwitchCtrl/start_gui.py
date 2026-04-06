import sys

try:
    from NetDrivers import RFSwitch
except ImportError:
    try:
        sys.path.append('../NetDrivers')
        from RFSwitch import RFSwitch
    except ImportError:
        print("Cannot find the RF Switch driver")
        exit()

try:
    from tkinter import *
    import tkinter.messagebox
except ImportError:
    from TKinter import *
    import TKinter.messagebox

## Instantiate the 4-port RF Switch
ip_4p = "192.168.0.196"
sw_4p = RFSwitch(ip_4p)

## Instantiate the 8-port RF Switch
ip_8p = "192.168.0.195"
sw_8p = RFSwitch(ip_8p)

## Geometry of the GUI
win_size_x  = 356
win_size_y  = 320

but_size_x  =  40
but_size_y  =   1

but1_pos_x  =   0
but1_pos_y  =  70

but2_pos_x  =   0
but2_pos_y  = 100

## Create the main window and storing the window object in 'win'
win=Tk() 

## Set the title of the window
win.title('LOUD RF Switch Contol')

## Set the size of the window
win.geometry( str(int(win_size_x)) + "x" + str(int(win_size_y)) )

## ========= PROBE FUNCTIONALITY ========= ##
lf_probe = LabelFrame(win, text='Probe Connection')
lf_probe.grid(row=0, column=0, columnspan=2, sticky=N+W)

## Create containers for the entry strings
sn4_str = StringVar()
mn4_str = StringVar()
sn8_str = StringVar()
mn8_str = StringVar()

## Add the labels and entries that get populated by probe
Label(lf_probe, text='4-port  RF  Switch  Model: ').grid(row=1, column=0)
Label(lf_probe, text='4-port  RF  Switch  Serial:').grid(row=2, column=0)
Label(lf_probe, text='8-port  RF  Switch  Model: ').grid(row=3, column=0)
Label(lf_probe, text='8-port  RF  Switch  Serial:').grid(row=4, column=0)
e1 = Entry(lf_probe, textvariable=mn4_str, state="disabled") ; e1.grid(row=1, column=1)
e2 = Entry(lf_probe, textvariable=sn4_str, state="disabled") ; e2.grid(row=2, column=1)
e3 = Entry(lf_probe, textvariable=mn8_str, state="disabled") ; e3.grid(row=3, column=1)
e4 = Entry(lf_probe, textvariable=sn8_str, state="disabled") ; e4.grid(row=4, column=1)

## Details of the "Probe" button
btn_probe=Button(lf_probe, text="Probe", 
    width   = but_size_x,
    height  = but_size_y,)
btn_probe.grid(row=0, column=0, columnspan=4)
## ======================================= ##

## ========== VNA FUNCTIONALITY ========== ##
lf_vna = LabelFrame(win, text='VNA Routing')
lf_vna.grid(row=1, column=0, sticky=N+W)

## Create containers for the entry strings
vna_cnx_str = StringVar()
vna_cnx_str.set("None")

r_kids = Radiobutton(lf_vna, text="Connect toward KIDs"  , state="disabled") ; r_kids.grid(row=0, column=0, sticky=N+W)
r_qbit = Radiobutton(lf_vna, text="Connect toward Qubits", state="disabled") ; r_qbit.grid(row=1, column=0, sticky=N+W)
Label(lf_vna, text='VNA toward: ').grid(row=2, column=0, sticky=N+W)
e5 = Entry(lf_vna, textvariable=vna_cnx_str, state="disabled") ; e5.grid(row=3, column=0, sticky=N+W)
## ======================================= ##

## ========== KID FUNCTIONALITY ========== ##
lf_kid = LabelFrame(win, text='KID Routing')
lf_kid.grid(row=1, column=1, sticky=N+W)

## Create containers for the entry strings
kid_cnx_str = StringVar()
kid_cnx_str.set("None")

# r_kid_nil = Radiobutton(lf_kid, text="Connect to None" , state="disabled") ; r_kid_nil.grid(row=0, column=0, sticky=N+W)
r_kid_vna = Radiobutton(lf_kid, text="Connect to VNA"  , state="disabled") ; r_kid_vna.grid(row=0, column=0, sticky=N+W)
r_kid_zcu = Radiobutton(lf_kid, text="Connect to RFSOC", state="disabled") ; r_kid_zcu.grid(row=1, column=0, sticky=N+W)
Label(lf_kid, text='KID connected to: ').grid(row=2, column=0, sticky=N+W)
e6 = Entry(lf_kid, textvariable=kid_cnx_str, state="disabled") ; e6.grid(row=3, column=0, sticky=N+W)
## ======================================= ##

# ========= QUBIT FUNCTIONALITY ========= ##
lf_qbits = LabelFrame(win, text='Qubit Routing')
lf_qbits.grid(row=2, column=0, columnspan=2, sticky=N+W)

## Create a group for the Silicon qubit
lf_qbit_Si = LabelFrame(lf_qbits, text='Silicon Routing')
lf_qbit_Si.grid(row=0, column=0, sticky=N+W)

Si_qbit_cnx_str = StringVar()
Si_qbit_cnx_str.set("None")

# r_Si_qbit_nil = Radiobutton(lf_qbit_Si, text="Connect to None" , state="disabled") ; r_Si_qbit_nil.grid(row=0, column=0, sticky=N+W)
r_Si_qbit_vna = Radiobutton(lf_qbit_Si, text="Connect to VNA"  , state="disabled") ; r_Si_qbit_vna.grid(row=0, column=0, sticky=N+W)
r_Si_qbit_zcu = Radiobutton(lf_qbit_Si, text="Connect to RFSOC", state="disabled") ; r_Si_qbit_zcu.grid(row=1, column=0, sticky=N+W)
Label(lf_qbit_Si, text='Si qubit connected to: ').grid(row=2, column=0, sticky=N+W)
e7 = Entry(lf_qbit_Si, textvariable=Si_qbit_cnx_str, state="disabled") ; e7.grid(row=3, column=0, sticky=N+W)

## Create a group for the Sapphire qubit
lf_qbit_Sp = LabelFrame(lf_qbits, text='Sapphire Routing')
lf_qbit_Sp.grid(row=0, column=1, sticky=N+W)

Sp_qbit_cnx_str = StringVar()
Sp_qbit_cnx_str.set("None")

# r_Sp_qbit_nil = Radiobutton(lf_qbit_Sp, text="Connect to None" , state="disabled") ; r_Sp_qbit_nil.grid(row=0, column=0, sticky=N+W)
r_Sp_qbit_vna = Radiobutton(lf_qbit_Sp, text="Connect to VNA"  , state="disabled") ; r_Sp_qbit_vna.grid(row=0, column=0, sticky=N+W)
r_Sp_qbit_zcu = Radiobutton(lf_qbit_Sp, text="Connect to RFSOC", state="disabled") ; r_Sp_qbit_zcu.grid(row=1, column=0, sticky=N+W)
Label(lf_qbit_Sp, text='Saph qubit connected to: ').grid(row=2, column=0, sticky=N+W)
e8 = Entry(lf_qbit_Sp, textvariable=Sp_qbit_cnx_str, state="disabled") ; e8.grid(row=3, column=0, sticky=N+W)
# ======================================= ##

# def spoof():
#     return "spoofed", "spoofed"

## Probe Button function
def func_probe():
    mn4, sn4 = sw_4p.TestConnection()
    mn4_str.set(mn4)#"ModelNumber")
    sn4_str.set(sn4)#"SerialNumber")

    mn8, sn8 = sw_8p.TestConnection()
    mn8_str.set(mn8)#"ModelNumber")
    sn8_str.set(sn8)#"SerialNumber")

    ## Only enable radio buttons if we got a response
    if (mn8 != "No Response!") and (mn4 != "No Response!"):
        r_kids["state"] = "normal"
        r_qbit["state"] = "normal"
        r_kids.deselect()
        r_qbit.deselect()

        # r_kid_nil["state"]  = "normal"
        r_kid_vna["state"] = "normal"
        r_kid_zcu["state"] = "normal"
        r_kid_vna.deselect()
        r_kid_zcu.deselect()

        # r_Si_qbit_nil["state"]  = "normal"
        r_Si_qbit_vna["state"] = "normal"
        r_Si_qbit_zcu["state"] = "normal"
        r_Si_qbit_vna.deselect()
        r_Si_qbit_zcu.deselect()

        # r_Sp_qbit_nil["state"]  = "normal"
        r_Sp_qbit_vna["state"] = "normal"
        r_Sp_qbit_zcu["state"] = "normal"
        r_Sp_qbit_vna.deselect()
        r_Sp_qbit_zcu.deselect()
btn_probe["command"] = func_probe

## Connect VNA toward KID Button function
def func_vna_to_kid():
    vna_cnx_str.set("KID")
    r_kids["state"] = "disabled"
    r_qbit["state"] = "normal"

    if(sw_4p.SetSwitchState("A", 2)):
        tkinter.messagebox.showinfo("Error",sw_4p.error)
    if(sw_4p.SetSwitchState("B", 2)):
        tkinter.messagebox.showinfo("Error",sw_4p.error)
r_kids['command'] = func_vna_to_kid

## Connect VNA toward Qubits Button function
def func_vna_to_qubits():
    vna_cnx_str.set("Qubits")
    r_kids["state"] = "normal"
    r_qbit["state"] = "disabled"

    if(sw_4p.SetSwitchState("A", 1)):
        tkinter.messagebox.showinfo("Error",sw_4p.error)
    if(sw_4p.SetSwitchState("B", 1)):
        tkinter.messagebox.showinfo("Error",sw_4p.error)
r_qbit['command'] = func_vna_to_qubits

## Connect the KID to the VNA channels
def func_kid_to_vna():
    kid_cnx_str.set("VNA")
    # r_kid_nil["state"]  = "disabled"
    r_kid_vna["state"] = "disabled"
    r_kid_zcu["state"] = "normal"

    if(sw_4p.SetSwitchState("C", 2)):
        tkinter.messagebox.showinfo("Error",sw_4p.error)
    if(sw_4p.SetSwitchState("D", 2)):
        tkinter.messagebox.showinfo("Error",sw_4p.error)
r_kid_vna['command'] = func_kid_to_vna

## Connect the KID to the RF-SoC channels
def func_kid_to_rfsoc():
    kid_cnx_str.set("RF-SoC")
    # r_kid_nil["state"]  = "disabled"
    r_kid_vna["state"] = "normal"
    r_kid_zcu["state"] = "disabled"

    if(sw_4p.SetSwitchState("C", 1)):
        tkinter.messagebox.showinfo("Error",sw_4p.error)
    if(sw_4p.SetSwitchState("D", 1)):
        tkinter.messagebox.showinfo("Error",sw_4p.error)
r_kid_zcu['command'] = func_kid_to_rfsoc

## Connect the Si qubit to the VNA channels
def func_siq_to_vna():
    Si_qbit_cnx_str.set("VNA")
    # r_Si_qbit_nil["state"]  = "disabled"
    r_Si_qbit_vna["state"] = "disabled"
    r_Si_qbit_zcu["state"] = "normal"

    if(sw_8p.SetSwitchState("A", 1)):
        tkinter.messagebox.showinfo("Error",sw_8p.error)
    if(sw_8p.SetSwitchState("C", 1)):
        tkinter.messagebox.showinfo("Error",sw_8p.error)

    if(sw_8p.SetSwitchState("B", 1)):
        tkinter.messagebox.showinfo("Error",sw_8p.error)
    if(sw_8p.SetSwitchState("D", 1)):
        tkinter.messagebox.showinfo("Error",sw_8p.error)
r_Si_qbit_vna['command'] = func_siq_to_vna

## Connect the Si qubit to the RF-SoC channels
def func_siq_to_rfsoc():
    Si_qbit_cnx_str.set("RF-SoC")
    # r_Si_qbit_nil["state"]  = "disabled"
    r_Si_qbit_vna["state"] = "normal"
    r_Si_qbit_zcu["state"] = "disabled"

    if(sw_8p.SetSwitchState("B", 2)):
        tkinter.messagebox.showinfo("Error",sw_8p.error)
    if(sw_8p.SetSwitchState("D", 2)):
        tkinter.messagebox.showinfo("Error",sw_8p.error)
r_Si_qbit_zcu['command'] = func_siq_to_rfsoc

## Connect the Saph qubit to the VNA channels
def func_spq_to_vna():
    Sp_qbit_cnx_str.set("VNA")
    # r_Sp_qbit_nil["state"]  = "disabled"
    r_Sp_qbit_vna["state"] = "disabled"
    r_Sp_qbit_zcu["state"] = "normal"

    if(sw_8p.SetSwitchState("A", 2)):
        tkinter.messagebox.showinfo("Error",sw_8p.error)
    if(sw_8p.SetSwitchState("C", 2)):
        tkinter.messagebox.showinfo("Error",sw_8p.error)

    if(sw_8p.SetSwitchState("F", 1)):
        tkinter.messagebox.showinfo("Error",sw_8p.error)
    if(sw_8p.SetSwitchState("H", 1)):
        tkinter.messagebox.showinfo("Error",sw_8p.error)
r_Sp_qbit_vna['command'] = func_spq_to_vna

## Connect the Saph qubit to the RF-SoC channels
def func_spq_to_rfsoc():
    Sp_qbit_cnx_str.set("RF-SoC")
    # r_Sp_qbit_nil["state"]  = "disabled"
    r_Sp_qbit_vna["state"] = "normal"
    r_Sp_qbit_zcu["state"] = "disabled"

    if(sw_8p.SetSwitchState("F", 2)):
        tkinter.messagebox.showinfo("Error",sw_8p.error)
    if(sw_8p.SetSwitchState("H", 2)):
        tkinter.messagebox.showinfo("Error",sw_8p.error)
r_Sp_qbit_zcu['command'] = func_spq_to_rfsoc




## Execute
win.mainloop() #running the loop that works as a trigger
