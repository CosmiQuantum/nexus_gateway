import socket
from urllib.request import urlopen
from time import sleep

class NetDevice():

    def __init__(self,server_ip="192.168.0.142",server_port=1234):
        self.address   = (server_ip, server_port)

    ## Sends a command to the server address and returns an array of 
    ## strings containing the parts of the server response string
    ## between the commas
    def _sendCmd(self,cmd,getResponse=True,verbose=False):
        ## Append a newline character to the end of the line
        if not (cmd[-1]=="\n"):
            cmdStr = cmd+"\n"

        ## Diagnostic text
        if verbose:
            print("Sending command:",cmd,"to IP:",self.address)

        ## Open the socket and send/receive data
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.address)
                s.settimeout(1)
                s.sendall(cmdStr.encode())
                if(getResponse):
                    data   = s.recv(1024)
                    retStr = data.decode()
                    if verbose:
                        print("Received:", retStr)
                else:
                    retStr = ""
        except socket.timeout:
            print("Timeout on", self.address[0])
            return

        ## Remove leading or trailing whitespace in string response
        ## as well as any quotation marks
        retStr   = retStr.strip().strip("\'").strip("\"")

        ## Return the split comma-separated response
        sleep(0.05)
        if (getResponse):
            return retStr.split(",")

    ## Checks to see if there's communication on the server address
    def testConnection(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect(self.address)
            except ConnectionRefusedError:
                print("ERROR -- Connection refused by remote host")
            except OSError:
                print("ERROR -- No route to host, check IP address")
            except socket.timeout:
                print("Timeout on", self.server_address[0])
            else:
                print("Connection OK")
        return

    ## Get the standard Identity string of the device
    def getIdentity(self):
        resp = self._sendCmd("*IDN?")
        return resp ## array of strings

    ## Clear any errors on the device
    def clearErrors(self):
        self._sendCmd("*CLS", getResponse=False)
        return 
        
    ## Perform a soft reset of the device
    def doSoftReset(self):
        self._sendCmd("*RST", getResponse=False)
        return 

class NetGPIBDevice(NetDevice):

    def __init__(self,server_ip="192.168.0.142",server_port=1234,gpib_addr=11):
        self.address   = (server_ip, server_port)
        self.gpib_addr = gpib_addr

    ## Sends a command to the server address and returns an array of 
    ## strings containing the parts of the server response string
    ## between the commas
    def _sendCmd(self,cmd,getResponse=True,verbose=False):
        ## Append a newline character to the end of the line
        if not (cmd[-1]=="\n"):
            cmdStr = cmd+"\n"

        ## Diagnostic text
        if verbose:
            print("Sending command:",cmd,"to IP:",self.address)

        ## Open the socket and send/receive data
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.address)
                s.settimeout(1)
                s.sendall(cmdStr.encode())
                if(getResponse):
                    s.sendall("++read\n".encode())
                    data   = s.recv(1024)
                    retStr = data.decode()
                    if verbose:
                        print("Received:", retStr)
                else:
                    retStr = ""
        except socket.timeout:
            print("Timeout on", self.address[0])
            return

        ## Remove leading or trailing whitespace in string response
        ## as well as any quotation marks
        retStr   = retStr.strip().strip("\'").strip("\"")

        ## Return the split comma-separated response
        sleep(0.05)
        if (getResponse):
            return retStr.split(",")

    ## Call this once after instantiating the class
    def configureGPIB(self):
        ## Set mode as CONTROLLER
        self._sendCmd("++mode 1", getResponse=False)

        ## Turn off read-after-write to avoid "Query Unterminated" errors
        self._sendCmd("++auto 0", getResponse=False)

        ## Do not append CR or LF to GPIB data
        self._sendCmd("++eos 3", getResponse=False)

        ## Assert EOI with last byte to indicate end of data
        self._sendCmd("++eoi 1", getResponse=False)

        ## Read timeout is 500 msec
        self._sendCmd("++read_tmo_ms 500", getResponse=False)

        return

    ## Call this before sending any commands to ensure the GPIB-LAN interface
    ## is focusing on the correct instrument via its GPIB address
    def focusInstrument(self):
        ## Set HP E3631A address
        self._sendCmd("++addr " + str(int(self.gpib_addr)), getResponse=False)
        return

class HttpDevice():

    error = "None"

    def __init__(self, ip_addr):

        if (len(ip_addr.split("."))==4):
            self.ip_addr = ip_addr
        else:
            self.ip_addr = None

    def HTTPSendCommandGetResponse(self, cmd_to_send, verbose=False):

        # Specify the IP address of the switch box
        full_msg = "http://" + self.ip_addr + "/" + cmd_to_send
        
        # Show the user the full message if they want
        if (verbose):
            print("Preparing to send message:", full_msg)

        # Send the HTTP command and try to read the result
        try:
            http_result = urlopen(full_msg, timeout=1)
            msg_return  = http_result.read().decode("utf-8")

            # Show the user the full response if they want
            if (verbose):
                print("Response from message:", msg_return)

            # The switch displays a web GUI for unrecognised commands
            #if len(msg_return) > 100:
            if (msg_return[0:3] == '-99'):
                self.error = "Error, unknown command not found: "+cmd_to_send
                print(self.error)
                msg_return = "Invalid Command!"

        # Catch an exception if URL is incorrect (incorrect IP or disconnected)
        except:
            self.error = "Error, no response from device; check IP address and connections."
            print(self.error)
            msg_return = "No Response!"
            # sys.exit()      # Exit the script

        # Return the response
        return msg_return
