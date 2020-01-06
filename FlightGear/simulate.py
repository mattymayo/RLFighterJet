import gym
import json
import datetime as dt
import time
import tensorflow as tf

from stable_baselines.common.policies import MlpLstmPolicy, FeedForwardPolicy, LstmPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.vec_env import VecFrameStack, SubprocVecEnv
from stable_baselines import PPO2

from env.ScreenCapEnv import ScreenCapEnv

import pandas as pd



def make_env(value):
    """
    Utility function for multiprocessed env.

    :param env_id: (str) the environment ID
    :param num_env: (int) the number of environments you wish to have in subprocesses
    :param seed: (int) the inital seed for RNG
    :param rank: (int) index of the subprocess
    """
    def _init():
        env = ScreenCapEnv(5000 + 500*value, value)
        #env.port(5000 + value)
        return env
    return _init


num_environments = 4 #8 env's uses 100% of all cores
simulate_time = 10000
num_timesteps = 0
num_save_points = 0

# The algorithms require a vectorized environment to run
env = SubprocVecEnv([make_env(i) for i in range(num_environments)])

# Custom MLP policy of 3 layers of size 128 each for the actor and 3 layers of 128 for the critic,
# with 64 lstm layers

class CustomLSTMPolicy(LstmPolicy):
    def __init__(self, sess, ob_space, ac_space, n_env, n_steps, n_batch, n_lstm=64, reuse=False, **_kwargs):
        super().__init__(sess, ob_space, ac_space, n_env, n_steps, n_batch, n_lstm, reuse,
                         net_arch=[128, 'lstm', dict(vf=[128, 128, 128], pi=[128,128,128])],
                         layer_norm=True, feature_extraction="mlp", **_kwargs)


model = PPO2(CustomLSTMPolicy, env, verbose=1, tensorboard_log="./ppo2_flightgear_tensorboard_mango_flyer/")

# Use bash command tensorboard --logdir ./ppo2_flightgear_tensorboard_enemy_targeted_reward/



#model = PPO2.load("ScreenCapActor_mango_flyer2")



obs = env.reset()

for i in range(simulate_time):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    #env.render()
