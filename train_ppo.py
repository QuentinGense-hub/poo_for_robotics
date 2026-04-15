import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.logger import configure

from robot.pacman_env import PacmanEnv


TOTAL_TIMESTEPS = 2_000_000
N_ENVS = 4


def plot_training_loss(progress_csv: Path, output_path: Path) -> None:
    if not progress_csv.exists():
        print(f"Fichier de log introuvable: {progress_csv}")
        return

    timesteps = []
    losses = []

    with progress_csv.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            raw_loss = row.get("train/loss", "")
            raw_steps = row.get("time/total_timesteps", "")
            if not raw_loss or not raw_steps:
                continue

            try:
                loss = float(raw_loss)
                total_steps = int(float(raw_steps))
            except ValueError:
                continue

            timesteps.append(total_steps)
            losses.append(loss)

    if not losses:
        print("Aucune valeur de loss n'a ete trouvee dans progress.csv.")
        return

    plt.figure(figsize=(18, 5))
    plt.plot(timesteps, losses, color="tab:blue", linewidth=2)
    plt.title("Courbe de loss PPO")
    plt.xlabel("Timesteps")
    plt.ylabel("Loss")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    print(f"Courbe de loss enregistree dans {output_path}")


def main():
    project_dir = Path(__file__).resolve().parent
    log_dir = project_dir / "logs" / "ppo_pacman"
    log_dir.mkdir(parents=True, exist_ok=True)

    vec_env = make_vec_env(PacmanEnv, n_envs=N_ENVS)

    model = PPO("MlpPolicy", vec_env, verbose=1)
    model.set_logger(configure(str(log_dir), ["stdout", "csv"]))
    model.learn(total_timesteps=TOTAL_TIMESTEPS)
    model.save(project_dir / "ppo_pacman")

    vec_env.close()

    plot_training_loss(
        log_dir / "progress.csv",
        project_dir / "ppo_training_loss.png",
    )


if __name__ == "__main__":
    main()
