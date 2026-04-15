from pathlib import Path

import pygame
from stable_baselines3 import PPO

from robot.pacman_env import PacmanEnv
from robot.vue import VuePygame


def main():
    model_path = Path(__file__).with_name("ppo_pacman.zip")
    if not model_path.exists():
        raise FileNotFoundError(
            f"Modele introuvable: {model_path}. Lance d'abord l'entrainement PPO."
        )

    model = PPO.load(model_path)
    rl_env = PacmanEnv(max_steps=None)
    observation, _ = rl_env.reset()

    if model.observation_space.shape != rl_env.observation_space.shape:
        raise ValueError(
            "Le modele charge n'utilise pas la meme observation que PacmanEnv. "
            f"Modele: {model.observation_space.shape}, env: {rl_env.observation_space.shape}. "
            "Relance train_ppo.py pour reentrainer le PPO."
        )

    if model.action_space.shape != rl_env.action_space.shape:
        raise ValueError(
            "Le modele charge n'utilise pas la meme action que PacmanEnv. "
            f"Modele: {model.action_space.shape}, env: {rl_env.action_space.shape}. "
            "Relance train_ppo.py pour reentrainer le PPO."
        )

    scale = 40
    vue = VuePygame(
        int(rl_env.width * scale),
        int(rl_env.height * scale),
    )
    vue.scale = scale

    running = True
    fps = 20

    while running:
        vue.clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        action, _ = model.predict(observation, deterministic=True)
        observation, reward, terminated, truncated, info = rl_env.step(action)
        rl_env.pacman.display_orientation = rl_env.pacman.orientation

        vue.dessiner_environnement(rl_env.env)
        pygame.display.set_caption(
            "Modele PPO omni | "
            f"Score: {rl_env.pacman.score} | dots: {len(rl_env.env.points)} | "
            f"vx={info['vx_cmd']:.2f} vy={info['vy_cmd']:.2f} w={info['omega_cmd']:.2f}"
        )

        if terminated or truncated:
            observation, _ = rl_env.reset()
            rl_env.pacman.display_orientation = rl_env.pacman.orientation

    pygame.quit()


if __name__ == "__main__":
    main()
