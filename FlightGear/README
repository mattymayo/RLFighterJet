# RLFighterJet
This is a RL environment that utilizes OpenAI baselines or stable-baselines to train a fighter jet to fly and eventually dogfight

## What's included
This project was developed and submitted to darpa for a proposal. As such, certain aspects of the code have been modified or removed. In it's current state, this repo simply needs someone to properly install FlightGear on a linux machine to begin training (in addition to installing everything needed for openAI baselines and gym.

## Performance and complexity
The performance of fully developed models is confidential and cannot be commented on. With that in mind, it takes a signficant amount of training and some fairly complex reward functions to get the desired effect. The model is trained in a very unique and experimental scenario in addition to being a very complex action space with signficant and physics-based interactions.

## What does the plane see?
Because we are using an auxillary flight simulator (FlightGear) and not the gym environment itself, a series of hooks were needed to allow the agents to both see and interact with the environment. By exploiting FG's telnet system, we are able to read data out from the simulator as well as set certain control values. By adjusting the frequency that telnet functions we were able to acheive near real-time data readouts over telnet. The plane's observation space is a set of 18 variables described as:
```python
        obs[0] = self.fgtn.getprop("/position/latitude-deg")`
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
```
