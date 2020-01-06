import random
from threading import Thread
import json
import gym
from gym import spaces
import pandas as pd
import numpy as np
import os
import random
import execnet
import subprocess
import time
import Hooks

RESPONSE_THRESHOLD=0.5
CURR_REWARD= 0
NUM_RWRD_OBS = 0
AVG_RWRD = 0
OBSERVATION = 0
NUM_SIM_STEPS = 0
PORT=0


class FlightGearEnv(gym.Env):
    """Generic env to take screen data and press keys"""
    metadata = {'python_2render.modes': ['human']}
    observation = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    hidden = np.zeros(3)
    def __init__(self, port, flag):
        self.reward_range = (-200,200)
        self.port=port
        self.flag=flag
	# Start flightgear sim and establish hooks, against other pilot

        time.sleep(flag/5)

        if (self.flag % 2 == 0):
            exec_string = "~/flightgear/dnc-managed/run_fgfs.sh --telnet=foo,bar,1000,foo,{},bar --aircraft=f15c --prop:/sim/rendering/multithreading-mode=AutomaticSelection --altitude=40000 --vc=400 --enable-fuel-freeze --geometry=300x300 --multiplay=out,10,127.0.0.1,{} --multiplay=in,10,127.0.0.1,{} --callsign=primary".format(self.port, self.port+1, self.port+501)
        else:
            exec_string = "~/flightgear/dnc-managed/run_fgfs.sh --telnet=foo,bar,1000,foo,{},bar --aircraft=f15c --prop:/sim/rendering/multithreading-mode=AutomaticSelection --altitude=40000 --vc=400 --enable-fuel-freeze --geometry=300x300 --multiplay=out,10,127.0.0.1,{} --multiplay=in,10,127.0.0.1,{} --callsign=primary".format(self.port, self.port+1, self.port-499)
        #os.system(exec_string)
        proc = subprocess.Popen([exec_string], shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)
        time.sleep(30)
        self.hooks = Hooks.Hooks(port)

        out = self.hooks.starter()

        print(out, file=open("output.txt", "a"))

	# Actions of the agent (control schema)
        self.action_space = spaces.MultiDiscrete([3,3,3,3])

	# Observations of the agent (observation schema)

        high = np.array([
            1000,1000,10000,1000,1000,1000,10000,10000,10000,10000,10000,10000,1000,1000,10000,1000,1000,1000])

        self.observation_space = spaces.Box(-high, high, dtype=np.float16)

    def next_observation(self):
	# Collection of variables from flightgear sim (nasal scripts vivek built)
        """
	Legend of variables in obs
	--------------------------
	0-lat, 1-lon
	2-altitude, 3-heading, 4-roll, 5-pitch
	6-uVelocity, 7-vVelocity, 8-wVelocity

	Legend of enemy variables in obs
	--------------------------------
	9-uVelocity, 10-vVelocity, 11-wVelocity, 12-lat, 13-lon
	14-altitude, 15-heading, 16-roll, 17-pitch

        """
        obs = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], dtype=float)
	# lots of code needs to go here to get all of the variables (just setting obs)
        obs = self.hooks.grab_data()
        #hidden = self.hooks.grab_hidden()
        observation = obs
        return obs

    def take_action(self, action):
	# iterate over action variables, and execute command if triggered
	# action will be a vector of probabilities for perfroming the mapped action
	# if the variable (-1-1) is above a threshold, it should be activated in the plane

        self.hooks.control_surfaces(action)
        # temp = 0


    def step(self, action):
        """

        Parameters
        ----------
        action :

        Returns
        -------
        ob, reward, episode_over, info : tuple
            ob (object) :
                an environment-specific object representing your observation of
                the environment.
            reward (float) :
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_over (bool) :
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info (dict) :
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
        """
        self.take_action(action)
        reward = self.get_reward()
        obs = self.next_observation()
        self.observation = obs
        self.hidden = self.hooks.grab_hidden()
        episode_over = False
        #print("my altitude = {}".format(obs[5]))
        #print("enemry lon = {}".format(obs[17]))
        check = self.hooks.check_freefall()
        if (check):
            episode_over = True
        if (obs[2] < 5000):
            episode_over = True


        #print("-----END OF STEP-----")
        return obs, reward, episode_over, {}

    def reset(self):
	# reset environment (execute commands, similar to __init__)
	# os.system("/usr/games/fgfs --httpd=5400 --aircraft=f15c")
        out = self.hooks.restarter2()
        return self.next_observation()

    def render(self, mode='human', close=False):
        print(f'Number of simulation steps: {NUM_SIM_STEPS}')
        print(f'Current Reward: {CURR_REWARD}')
        print(f'Number of Reward Observations: {NUM_RWRD_OBS}')
        print(f'Average Reward: {AVG_RWRD}')


    def get_reward(self):
        # give rewards for end states (we shot down the plane or got shot down)


        """We now need to characterize a mid-flight reward system"""


        """Here is a reward solely based on positioning and heading"""
        """	# get relative position
        rel_enemy_lat = self.observation[0] - self.observation[12]
        rel_enemy_lon = self.observation[1] - self.observation[13]
        heading = self.observation[3] / 180
        #print("rel_enemy_lat = {}".format(rel_enemy_lat))

        rel_my_lat = -rel_enemy_lat
        rel_my_lon = -rel_enemy_lon
        enemy_heading = self.observation[15] / 180



        rad2 = np.arctan2(rel_my_lon , rel_my_lat)
        enemy_rad = (enemy_heading*np.pi) - np.pi

        rad = np.arctan2(rel_enemy_lon , rel_enemy_lat)
        my_rad = (heading*np.pi) - np.pi
        reward = (np.cos(my_rad - rad)*15 / np.pi) - (np.cos(enemy_rad - rad2)*15 / np.pi)


        #print("rad = {}".format(rad))
        #print("my_rad = {}".format(my_rad))
        print("reward = {}".format(reward))

        return reward

        """

        # basic altitude control
        
        reward = 40 - np.abs(self.observation[4])/9 - np.abs(self.observation[5])/4.5 - np.abs(35000 - self.observation[2])/1000 - np.abs(self.observation[8])/200 - np.abs(self.hidden[0]) - np.abs(self.hidden[1]) - np.abs(self.hidden[2])
        print("reward = {}".format(reward))
        return reward
        
