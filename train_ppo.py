import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from gymnasium.utils.env_checker import check_env
from robot.pacman_env import PacmanEnv

env = gym.make("PacmanPPO-v0")
check_env(env.unwrapped)

vec_env = make_vec_env("PacmanPPO-v0", n_envs=4)

model = PPO("MlpPolicy", vec_env, verbose=1)
model.learn(total_timesteps=20000)