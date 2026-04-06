from .NetDevice import NetDevice

class E3631A(NetDevice):

    ## Query if the output is currently on or off
    def getOutputState(self):
        resp = self._sendCmd("OUTPut?")
        if resp is not None:
            return resp[0] ## "1" or "0"
        return

    ## Set the output state
    def setOutputState(self, enable=True, confirm=True):
        cmd  = "OUTPut"
        arg  = "ON" if enable else "OFF"
        cmd_str = " ".join( ( cmd, arg ) )
        self._sendCmd(cmd_str, getResponse=False)
        if confirm:
            print("Output is:", "ON" if bool(int(self.getOutputState())) else "OFF")
        return

    ## Get the current output settings
    def getVoltage(self, ch="P6V"):
        ## First check that the channel provided is okay
        if not (ch=="P6V" or ch=="P25V" or ch=="N25V"):
            print("Error:", ch, "is not a valid channel string. Options: P6V, P25V, N25V")
            return

        resp = self._sendCmd("APPLy? "+ch)
        return resp

    ## Apply a voltage/current on a specific output
    def setVoltage(self, voltage, current_limit=1.0, ch="P6V", confirm=True):

        ## First check that the channel provided is okay
        if not (ch=="P6V" or ch=="P25V" or ch=="N25V"):
            print("Error:", ch, "is not a valid channel string. Options: P6V, P25V, N25V")
            return

        ## Parse the voltage and current values
        vlt_str = "{:.3f}".format(voltage)
        cur_str = "{:.3f}".format(current_limit)
        if ( ch=="P6V" ):
            if voltage < 0.0:
                vlt_str = "MIN"
            if voltage > 6.0:
                vlt_str = "MAX"
            if current_limit < 0.0:
                cur_str = "MIN"
            if current_limit > 5.0:
                cur_str = "MAX"

        if ( ch=="P25V" ):
            if voltage < 0.0:
                vlt_str = "MIN"
            if voltage > 25.0:
                vlt_str = "MAX"
            if current_limit < 0.0:
                cur_str = "MIN"
            if current_limit > 1.0:
                cur_str = "MAX"

        ## This may not work as expected depending on if the firmware
        ## expects a negative sign in the command
        if ( ch=="N25V" ):
            if voltage > 0.0:
                vlt_str = "MIN"
            if voltage < -25.0:
                vlt_str = "MAX"
            if current_limit < 0.0:
                cur_str = "MIN"
            if current_limit > 1.0:
                cur_str = "MAX"

        ## Define the command string to send
        cmd  = "APPLy"
        args = ( ch, vlt_str, cur_str )
        cmd_str = " ".join( ( cmd, ",".join(args) ) )

        ## If we're on the right channel, apply the voltage
        self._sendCmd(cmd_str, getResponse=False)

        if confirm:
            resp = self.getVoltage(ch=ch)
            print("Settings:", resp)

    def measureVoltage(self, ch="P6V"):
        ## First check that the channel provided is okay
        if not (ch=="P6V" or ch=="P25V" or ch=="N25V"):
            print("Error:", ch, "is not a valid channel string. Options: P6V, P25V, N25V")
            return

        resp = self._sendCmd("MEASure:VOLTage? "+ch)
        return resp

    def measureCurrent(self, ch="P6V"):
        ## First check that the channel provided is okay
        if not (ch=="P6V" or ch=="P25V" or ch=="N25V"):
            print("Error:", ch, "is not a valid channel string. Options: P6V, P25V, N25V")
            return

        resp = self._sendCmd("MEASure:CURRent? "+ch)
        return resp