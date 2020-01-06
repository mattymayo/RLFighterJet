from FGTelnet import FGTelnet
import time
import sys
import numpy as np

class Hooks:
    def __init__(self, port):
        self.fgtn=FGTelnet("localhost", port)
        self.obs = self.grab_data()

    def starter(self):

        self.fgtn.setprop("/sim/current-view/view-number", 1)
        self.fgtn.setprop("/sim/current-view/view-number", 0)
        self.fgtn.setprop("/controls/engines/engine[0]/throttle", 0.9)
        self.fgtn.setprop("/controls/engines/engine[1]/throttle", 0.9)

    def restarter(self):

        self.fgtn.setprop("/sim/current-view/view-number", 1)
        self.fgtn.setprop("/sim/current-view/view-number", 0)
        self.fgtn.setprop("/position/altitude-ft", 40000)
        self.fgtn.setprop("/controls/flight/aileron", 0)
        self.fgtn.setprop("/controls/flight/elevator", 0)
        self.fgtn.setprop("/controls/flight/rudder", 0)
        self.fgtn.setprop("/orientation/roll-deg", 0)
        self.fgtn.setprop("/orientation/pitch-deg", 0)
        self.fgtn.setprop("/velocities/speed-down-fps", 0)

    def restarter2(self):
        #self.fgtn.sendcmd("pause")
        self.fgtn.setprop("/sim/current-view/view-number", 1)
        self.fgtn.setprop("/sim/current-view/view-number", 0)
        self.fgtn.setprop("/position/altitude-ft", 40000)
        self.fgtn.setprop("/position/latitude-deg", 63.9)
        self.fgtn.setprop("/position/longitude-degr", -23.6)
        self.fgtn.setprop("/orientation/roll-deg", 0)
        self.fgtn.setprop("/orientation/pitch-deg", 0)
        self.fgtn.setprop("/orientation/heading-deg", 0)
        self.fgtn.setprop("/velocities/uBody-fps", 0)
        self.fgtn.setprop("/velocities/vBody-fps", 0)
        self.fgtn.setprop("/velocities/wBody-fps", 0)
        self.fgtn.setprop("/orientation/pitch-rate-degps", 0)
        self.fgtn.setprop("/orientation/roll-rate-degps", 0)
        self.fgtn.setprop("/velocities/airspeed-kt", 400)
        self.fgtn.setprop("/orientation/roll-rate-degps", 0)
        self.fgtn.setprop("/orientation/pitch-rate-degps", 0)
        self.fgtn.setprop("/orientation/yaw-rate-degps", 0)
        self.fgtn.setprop("/controls/flight/aileron", 0)
        self.fgtn.setprop("/controls/flight/elevator", 0)
        self.fgtn.setprop("/controls/flight/rudder", 0)
        #self.fgtn.sendcmd("unpause")

        ###set enemy position, orientation, velocity
        """self.fgtn.setprop("/ai/models/multiplayer/position/latitude-deg", 64)#something higher
        self.fgtn.setprop("/ai/models/multiplayer/position/longitude-deg", -23.6)
        self.fgtn.setprop("/ai/models/multiplayer/position/altitude-ft", 40000)
        self.fgtn.setprop("/ai/models/multiplayer/velocities/uBody-fps", -300)
        self.fgtn.setprop("/ai/models/multiplayer/velocities/vBody-fps", 0)
        self.fgtn.setprop("/ai/models/multiplayer/velocities/wBody-fps", 0)
        self.fgtn.setprop("/ai/models/multiplayer/orientation/true-heading-deg", 180)
        self.fgtn.setprop("/ai/models/multiplayer/orientation/roll-deg", 0)
        self.fgtn.setprop("/ai/models/multiplayer/orientation/pitch-deg", 0)"""


    def grab_hidden(self):
        hidden = np.zeros(3)
        hidden[0] = self.fgtn.getprop("/orientation/pitch-rate-degps")
        hidden[1] = self.fgtn.getprop("/position/roll-rate-degps")
        hidden[2] = self.fgtn.getprop("/position/yaw-rate-degps")

        

    def grab_data(self):

        obs = np.zeros(18)
        obs[0] = self.fgtn.getprop("/position/latitude-deg")
        obs[1] = self.fgtn.getprop("/position/longitude-deg")
        obs[2] = self.fgtn.getprop("/position/altitude-ft")
        obs[3] = self.fgtn.getprop("/orientation/heading-deg")
        obs[4] = self.fgtn.getprop("/orientation/roll-deg")
        obs[5] = self.fgtn.getprop("/orientation/pitch-deg")
        obs[6] = self.fgtn.getprop("/velocities/uBody-fps")
        obs[7] = self.fgtn.getprop("/velocities/vBody-fps")
        obs[8] = self.fgtn.getprop("/velocities/wBody-fps")
        obs[9] = self.fgtn.getprop("/ai/models/multiplayer/velocities/uBody-fps")
        obs[10] = self.fgtn.getprop("/ai/models/multiplayer/velocities/vBody-fps")
        obs[11] = self.fgtn.getprop("/ai/models/multiplayer/velocities/wBody-fps")
        obs[12] = self.fgtn.getprop("/ai/models/multiplayer/position/latitude-deg")
        obs[13] = self.fgtn.getprop("/ai/models/multiplayer/position/longitude-deg")
        obs[14] = self.fgtn.getprop("/ai/models/multiplayer/position/altitude-ft")
        obs[15] = self.fgtn.getprop("/ai/models/multiplayer/orientation/true-heading-deg")
        obs[16] = self.fgtn.getprop("/ai/models/multiplayer/orientation/roll-deg")
        obs[17] = self.fgtn.getprop("/ai/models/multiplayer/orientation/pitch-deg")


        
        return obs

    def aileron_control(self, flag):

        if (flag ==1):
            temp = float(self.fgtn.getprop("/controls/flight/aileron"))
            self.fgtn.setprop("/controls/flight/aileron", temp + 0.05)
        elif(flag == 2):
            temp = float(self.fgtn.getprop("/controls/flight/aileron"))
            self.fgtn.setprop("/controls/flight/aileron", temp - 0.05)

    def elevator_control(self, flag):

        if (flag == 1):
            temp = float(self.fgtn.getprop("/controls/flight/elevator"))
            self.fgtn.setprop("/controls/flight/elevator", temp + 0.05)
        elif(flag == 2):
            temp = float(self.fgtn.getprop("/controls/flight/elevator"))
            self.fgtn.setprop("/controls/flight/elevator", temp - 0.05)


    def rudder_control(self, flag):

        if (flag ==1):
            temp = float(self.fgtn.getprop("/controls/flight/rudder"))
            self.fgtn.setprop("/controls/flight/rudder", temp + 0.05)
        elif(flag == 2):
            temp = float(self.fgtn.getprop("/controls/flight/rudder"))
            self.fgtn.setprop("/controls/flight/rudder", temp - 0.05)

    def throttle_control(self, flag):

        if (flag ==1):
            temp = float(self.fgtn.getprop("/controls/engines/engine[0]/throttle"))
            self.fgtn.setprop("/controls/engines/engine[0]/throttle", temp + 0.05)
            temp2 = float(self.fgtn.getprop("/controls/engines/engine[1]/throttle"))
            self.fgtn.setprop("/controls/engines/engine[1]/throttle", temp + 0.05)
        elif(flag == 2):
            temp = float(self.fgtn.getprop("/controls/engines/engine[0]/throttle"))
            self.fgtn.setprop("/controls/engines/engine[0]/throttle", temp - 0.05)
            temp2 = float(self.fgtn.getprop("/controls/engines/engine[1]/throttle"))
            self.fgtn.setprop("/controls/engines/engine[1]/throttle", temp - 0.05)

    def control_surfaces(self, action):
        #action space is a 1 by 4 array where each index is a control, 2 means decrease, 1 means increase, 0 is no action
        self.aileron_control(action[0])
        self.elevator_control(action[1])
        self.rudder_control(action[2])
        self.throttle_control(action[3])
        

    def check_freefall(self):
        temp = float(self.fgtn.getprop("/velocities/speed-down-fps"))
        roll = float(self.fgtn.getprop("/orientation/roll-rate-degps"))
        yaw = float(self.fgtn.getprop("/orientation/yaw-rate-degps"))
        if (temp >= 500):
            return True
        elif (roll >= 30):
            return True
        elif (yaw >= 30):
            return True
        else:
            return False











