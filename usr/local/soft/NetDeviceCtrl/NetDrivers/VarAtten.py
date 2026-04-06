from .NetDevice import HttpDevice
from urllib.parse import quote

# https://adauratech.com/support/
class VarAtten(HttpDevice):

    device_info = {}

    def SendCmd(self, cmd_to_send, verbose=False):
        command = "execute.php?"+cmd_to_send
        whitespace_corrected_command = quote(command,safe=':/?') 
        return self.HTTPSendCommandGetResponse(whitespace_corrected_command,verbose=verbose)

    def GetDeviceInfo(self, verbose=False):
        info = self.SendCmd("INFO")

        lines = info.split("\r\n")
        for line in lines:
            if verbose:
                print(line)
            prts = line.split(":")
            if len(prts)==2:
                self.device_info[prts[0]] = prts[1]

        return info

    def GetChannelStatus(self, verbose=False):
        status = self.SendCmd("STATUS")

        if verbose:
            lines = status.split("\r\n")
            for line in lines:
                print(line)

        return status

    def Reset(self, verbose=False):
        return self.SendCmd("RESET")

    def Locate(self,verbose=False): #REL
        return self.SendCmd("LOCATE")
    
    def SetChannel(self, ch, val, verbose=False):
        ## Minimum attenuation:  0 dB
        ## Maximum attenuation: 95 dB
        ## Step size: 0.25 dB

        ## Get the channel string
        ch_int = int(ch)
        if ch_int > 8:
            print("Bad channel reference:",ch_int,"Maximum is 8")
            return "ERROR"
        if ch_int < 1:
            print("Bad channel reference:",ch_int,"Minimum is 1")
            return "ERROR"
        ch_str = '%i' % ch_int

        ## Get the attenuation value string
        if val > 95.0:
            val = 95.0
            print("Bad attenuation value:",val,"Maximum is 95.0 dB")
        if val < 0.0:
            val = 0.0
            print("Bad attenuation value:",val,"Minimum is 0.0 dB")

        def roundPartial(value, resolution):
            return round(value / resolution) * resolution

        val_rnd = roundPartial(val, 0.25)
        val_str = '%.2f' % val_rnd
        
        if verbose:
            print("Setting channel",ch_str,"to",val_str,"dB of attenuation.")

        cmd = " ".join(["SET",ch_str,val_str])
        if verbose:
            print("Sending command:", "\""+cmd+"\"")
        ans = self.SendCmd(cmd)

        if verbose:
            lines = ans.split("\r\n")
            for line in lines:
                print(line)

        return ans

    def SetAllChannels(self, vals, verbose=False):
        N_vals = 0
        try:
            N_vals = len(vals)
        except TypeError as e:
            N_vals = 1
            vals   = [vals]

        if (N_vals != 1) and (N_vals !=8):
            print("Wrong number of channel values:",N_vals,"Must be 1 or 8 values")
            return "ERROR"

        def roundPartial(value, resolution):
            return round(value / resolution) * resolution

        send_vals = [""]*int(N_vals)

        for i in range(N_vals):
            val_rnd = roundPartial(vals[i], 0.25)
            val_str = '%.2f' % val_rnd
            send_vals[i] = val_str

        cmd = " ".join(["SAA", " ".join(send_vals)])
        if verbose:
            print("Sending command:", "\""+cmd+"\"")
        ans = self.SendCmd(cmd)

        if verbose:
            lines = ans.split("\r\n")
            for line in lines:
                print(line)

        return ans



