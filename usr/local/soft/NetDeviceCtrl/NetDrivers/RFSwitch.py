from .NetDevice import HttpDevice

class RFSwitch(HttpDevice):

    def SendCmd(self, cmd_to_send, verbose=False):
        return self.HTTPSendCommandGetResponse(":"+cmd_to_send,verbose=verbose)

    def TestConnection(self):
        model = self.SendCmd("MN?")       # Get model name
        serln = self.SendCmd("SN?")       # Get serial number

        return model, serln

    def SetSwitchState(self, switch_id, out_port):

        # Check that we're only acting on switches that exist
        if not ( (switch_id=="A") or (switch_id=="B") or (switch_id=="C") or (switch_id=="D")
              or (switch_id=="E") or (switch_id=="F") or (switch_id=="G") or (switch_id=="H") ):
            self.error = "Error, unregonized switch ID:"+switch_id
            print(self.error)
            return True ## error state

        # Check that the out port is either 1 (left) or 2 (right)
        if not ( (out_port==1) or (out_port==2) ):
            self.error = "Error, unregonized port #:"+str(out_port)
            print(self.error)
            return True ## error state

        # The command expects a 0 or 1
        out_port = int(out_port - 1)

        # If we've made it this far our message is OK to send
        msg    = "SET"+switch_id+"="+str(out_port)
        status = self.SendCmd(msg, verbose=True)

        # Now query the state to ensure it worked
        resp  = self.SendCmd(switch_id+"SWPORT?", verbose=True)

        # Do some validity checks (response is an 8-bit number [MSB]HGFEDCBA[LSB])
        val = int(resp)
        bit_str = bin(val).split("b")[1].zfill(8)

        bits = { "A": bit_str[-1], "B": bit_str[-2],
                 "C": bit_str[-3], "D": bit_str[-4],
                 "E": bit_str[-5], "F": bit_str[-6],
                 "G": bit_str[-7], "H": bit_str[-8] }
        outp = int(bits[switch_id])

        print ("Switch", switch_id, "connected, Com =>", outp+1, "(VNA)" if outp+1 == 2 else "(USRP)")

        self.error = "Error, port did not change state"
        return  not(outp == out_port)

