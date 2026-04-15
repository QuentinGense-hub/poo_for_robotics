from pathlib import Path
import math

import pygame
from stable_baselines3 import PPO

from robot.pacman_env import PacmanEnv
from robot.vue import VuePygame


DISPLAY_ORIENTATIONS = {
    1: math.pi / 2,
    2: -math.pi / 2,
    3: math.pi,
    4: 0.0,
}


def main():
    model_path = Path(__file__).with_name("ppo_pacman.zip")
    if not model_path.exists():
        raise FileNotFoundError(
            f"Modele introuvable: {model_path}. Lance d'abord l'entrainement PPO."
        )

    model = PPO.load(model_path)
    rl_env = PacmanEnv()
    observation, _ = rl_env.reset()
    expected_obs_shape = model.observation_space.shape
    current_obs_shape = rl_env.observation_space.shape
    if expected_obs_shape != current_obs_shape:
        raise ValueError(
            "Le modele charge n'utilise pas la meme observation que PacmanEnv. "
            f"Modele: {expected_obs_shape}, env: {current_obs_shape}. "
            "Relance train_ppo.py pour reentrainer le PPO."
        )
    rl_env.pacman.display_orientation = 0.0

    scale = 40
    vue = VuePygame(
        int(rl_env.width * scale),
        int(rl_env.height * scale),
    )
    vue.scale = scale

    running = True
    fps = 15

    while running:
        vue.clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        action, _ = model.predict(observation, deterministic=True)
        observation, reward, terminated, truncated, _ = rl_env.step(int(action))
        if int(action) in DISPLAY_ORIENTATIONS:
            rl_env.pacman.display_orientation = DISPLAY_ORIENTATIONS[int(action)]

        vue.dessiner_environnement(rl_env.env)

        pygame.display.set_caption(
            f"Modele PPO | Score: {rl_env.pacman.score} | dots: {len(rl_env.env.points)}"
        )

        if terminated or truncated:
            observation, _ = rl_env.reset()
            rl_env.pacman.display_orientation = 0.0

    pygame.quit()


if __name__ == "__main__":
    main()
