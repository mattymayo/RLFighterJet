import gym
import json
import datetime as dt
import time
import tensorflow as tf

from stable_baselines.common.policies import MlpLstmPolicy, FeedForwardPolicy, LstmPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.vec_env import VecFrameStack, SubprocVecEnv
from stable_baselines import A2C

from env.FlightGearEnv import FlightGearEnv

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
        env = FllightGearEnv(5000 + 500*value, value)
        #env.port(5000 + value)
        return env
    return _init


num_environments = 4 #8 env's uses 100% of all cores
simulate_time = 0
num_timesteps = 100000
num_save_points = 1

# The algorithms require a vectorized environment to run
env = SubprocVecEnv([make_env(i) for i in range(num_environments)])

# Custom MLP policy of 3 layers of size 128 each for the actor and 3 layers of 128 for the critic,
# with 64 lstm layers

class CustomLSTMPolicy(LstmPolicy):
    def __init__(self, sess, ob_space, ac_space, n_env, n_steps, n_batch, n_lstm=64, reuse=False, **_kwargs):
        super().__init__(sess, ob_space, ac_space, n_env, n_steps, n_batch, n_lstm, reuse,
                         net_arch=[128, 'lstm', dict(vf=[64,64,64], pi=[64,64,64])],
                         layer_norm=True, feature_extraction="mlp", **_kwargs)


model = A2C(CustomLSTMPolicy, env, verbose=1, tensorboard_log="tensorboard/a2c_flightgear_tensorboard_mango_flyer2/")

# Use bash command tensorboard --logdir ./a2c_flightgear_tensorboard_mango_flyer2/


# model.load("ScreenCapActor_mango_flyer2")

inter_steps = int(num_timesteps/num_save_points)
i = 0

while i < num_save_points:
    model.learn(total_timesteps=inter_steps)
    model.save("models/a2c_FlightGearActor_mango_flyer2")
    print("Saving intermediate model with {} steps".format(inter_steps*(i+1)))
    i += 1


obs = env.reset()

for i in range(simulate_time):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    #env.render()
