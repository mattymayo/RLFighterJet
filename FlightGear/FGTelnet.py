import telnetlib

# FlightGear Telnet class in Python3
class FGTelnet:

    eol="\r\n".encode('ascii')

    def __init__(self, host, port):
        """
        Instantiates a FGTelnet object,
        opens connection and switche to data mode.
        Default to localhost at port 5401
        """
        self.host="localhost"
        self.port=port
        self.tn=telnetlib.Telnet()
        self.tn.set_debuglevel(0) #Debug
        self.tn.open(host, port)
        self.tn.write("data".encode('ascii')+FGTelnet.eol)

    def __message(self, text):
        """Creates ASCII coded message with EOL"""
        return text.encode('ascii')+FGTelnet.eol

    def getprop(self, prop):
        """
        Gets property
        prop -- path
        """
        self.tn.write(self.__message("get "+prop))
        return self.tn.read_until(FGTelnet.eol).decode('ascii').strip()
       

    def setprop(self, prop, value, type="s"):
        """
        Sets property
        prop --  path
        value -- property value
        type --  type: s=string, b=bool, i=int, d=double
        """
        if type=="b":
            self.tn.write(self.__message("setb "+prop+" "+str(value)))
        elif type=="i":
            self.tn.write(self.__message("seti "+prop+" "+str(value)))
        elif type=="d":
            self.tn.write(self.__message("setd "+prop+" "+str(value)))
        else:
            self.tn.write(self.__message("set "+prop+" "+str(value)))

    def sendcmd(self, text, reply=False):
        """
        Sends a command to the server
        text --  the command string
        reply -- If true the reply is read directly.
        Note: In data mode cd, set, run and unsubscribe does not create
        an echo reply but subscribe does. The listing command ls
        cannot be used with this method as it returns EOL after
        every item but no end of list marker in data mode.
        """
        self.tn.write(self.__message(text))
        if reply :
            return self.tn.read_until(FGTelnet.eol).decode('ascii').strip()
        else:
            return ""

    def readreply(self):
        """Reads a reply from the server """
        return self.tn.read_until(FGTelnet.eol).decode('ascii').strip()

    def close(self):
        print(self.tn.read_eager()) #Debug
        self.tn.close()

    def __del__(self):
        self.tn.close()

if __name__ == "__main__" :
    """Some test operations"""
    fgtn=FGTelnet("localhost", 5000)
    print(fgtn.host)
    fgtn.setprop("/tmp/teststring", "test")
    fgtn.setprop("/tmp/testbool", "true","b")
    fgtn.setprop("/tmp/testint", "256","i")
    fgtn.setprop("/tmp/testdouble", "3.1415","d")
    print(fgtn.getprop("/controls/engines/engine/cutoff"))
    print(fgtn.getprop("/controls/engines/engine/throttle"))
    fgtn.sendcmd("dump /position")
    print(fgtn.readreply()+"\n\n")
    #Subscribe echoes command so it has to be read and discarded
    fgtn.sendcmd("subscribe /tmp/teststring", True)
    print("Quit session and program by setting /tmp/teststring to end in FG")
    r=""
    while r != "/tmp/teststring=end":
        r=fgtn.readreply()
        print(r)
    fgtn.close()
