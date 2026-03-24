from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import EvalCallback

from robot.pacman_env import PacmanEnv

# Entraînement rapide, sans rendu
train_env = make_vec_env(PacmanEnv, n_envs=4, env_kwargs={"render_mode": None})

# Environnement séparé pour la visualisation
eval_env = PacmanEnv(render_mode="human")

eval_callback = EvalCallback(
    eval_env,
    best_model_save_path="./logs/best_model",
    log_path="./logs/",
    eval_freq=10_000,
    deterministic=True,
    render=True,
)

model = PPO("MlpPolicy", train_env, verbose=1)
model.learn(total_timesteps=200_000, callback=eval_callback)

model.save("ppo_pacman")
train_env.close()
eval_env.close()