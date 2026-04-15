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
SEED = 42


def linear_schedule(initial_value: float):
    def schedule(progress_remaining: float) -> float:
        return float(progress_remaining) * initial_value

    return schedule


def read_progress(progress_csv: Path) -> list[dict[str, str]]:
    if not progress_csv.exists():
        return []

    with progress_csv.open(newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def plot_metric(
    rows: list[dict[str, str]],
    metric_name: str,
    output_path: Path,
    title: str,
    ylabel: str,
) -> None:
    timesteps = []
    values = []

    for row in rows:
        raw_value = row.get(metric_name, "")
        raw_steps = row.get("time/total_timesteps", "")
        if not raw_value or not raw_steps:
            continue

        try:
            value = float(raw_value)
            total_steps = int(float(raw_steps))
        except ValueError:
            continue

        timesteps.append(total_steps)
        values.append(value)

    if not values:
        print(f"Aucune valeur trouvee pour {metric_name}.")
        return

    plt.figure(figsize=(12, 5))
    plt.plot(timesteps, values, color="tab:blue", linewidth=2)
    plt.title(title)
    plt.xlabel("Timesteps")
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    print(f"Courbe enregistree dans {output_path}")


def plot_monitor_rewards(monitor_dir: Path, output_path: Path) -> None:
    rewards = []
    lengths = []

    for monitor_file in sorted(monitor_dir.glob("*.monitor.csv")):
        with monitor_file.open(newline="", encoding="utf-8") as csv_file:
            next(csv_file, None)
            reader = csv.DictReader(csv_file)
            for row in reader:
                try:
                    rewards.append(float(row["r"]))
                    lengths.append(int(float(row["l"])))
                except (KeyError, ValueError):
                    continue

    if not rewards:
        print("Aucune recompense d'episode trouvee dans les fichiers monitor.")
        return

    cumulative_steps = []
    total_steps = 0
    for length in lengths:
        total_steps += length
        cumulative_steps.append(total_steps)

    plt.figure(figsize=(12, 5))
    plt.plot(cumulative_steps, rewards, color="tab:green", linewidth=1.5, alpha=0.8)
    plt.title("Reward par episode")
    plt.xlabel("Timesteps episodes")
    plt.ylabel("Reward episode")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    print(f"Courbe enregistree dans {output_path}")


def main():
    project_dir = Path(__file__).resolve().parent
    log_dir = project_dir / "logs" / "ppo_pacman"
    monitor_dir = log_dir / "monitor"
    log_dir.mkdir(parents=True, exist_ok=True)
    monitor_dir.mkdir(parents=True, exist_ok=True)

    vec_env = make_vec_env(
        PacmanEnv,
        n_envs=N_ENVS,
        seed=SEED,
        monitor_dir=str(monitor_dir),
    )

    model = PPO(
        "MlpPolicy",
        vec_env,
        verbose=1,
        seed=SEED,
        learning_rate=linear_schedule(3e-4),
        n_steps=1024,
        batch_size=256,
        n_epochs=10,
        gamma=0.995,
        gae_lambda=0.95,
        clip_range=0.15,
        ent_coef=0.005,
        vf_coef=0.5,
        max_grad_norm=0.5,
        target_kl=0.03,
        use_sde=True,
        sde_sample_freq=16,
        policy_kwargs=dict(net_arch=[128, 128]),
    )
    model.set_logger(configure(str(log_dir), ["stdout", "csv"]))
    model.learn(total_timesteps=TOTAL_TIMESTEPS, progress_bar=True)
    model.save(project_dir / "ppo_pacman")

    vec_env.close()

    rows = read_progress(log_dir / "progress.csv")
    plot_metric(
        rows,
        "train/loss",
        project_dir / "ppo_training_loss.png",
        "Courbe de loss PPO",
        "Loss",
    )
    plot_metric(
        rows,
        "rollout/ep_rew_mean",
        project_dir / "ppo_training_reward.png",
        "Reward moyen par episode",
        "Reward moyen",
    )
    plot_monitor_rewards(
        monitor_dir,
        project_dir / "ppo_training_episode_reward.png",
    )


if __name__ == "__main__":
    main()
