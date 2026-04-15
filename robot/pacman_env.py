import math

import gymnasium as gym
import numpy as np
from gymnasium import spaces
from gymnasium.envs.registration import register

from robot.environnement import Environnement
from robot.map_loader import creer_carte
from robot.moteur import MoteurOmnidirectionnel
from robot.pacman import Pacman


class PacmanEnv(gym.Env):
    register(
        id="PacmanPPO-v0",
        entry_point="robot.pacman_env:PacmanEnv",
    )

    def __init__(self, max_steps: int | None = 500):
        super().__init__()
        self.max_steps = max_steps

        # Commande continue d'un robot omnidirectionnel:
        # [vx, vy, omega] normalises dans [-1, 1].
        self.action_space = spaces.Box(
            low=-1.0,
            high=1.0,
            shape=(3,),
            dtype=np.float32,
        )

        # 8 rayons lidar + x, y + cos/sin(theta) + cible proche dans le repere robot
        # + distance cible + progression de collecte + score.
        self.observation_space = spaces.Box(
            low=-1.0,
            high=1.0,
            shape=(17,),
            dtype=np.float32,
        )

        self.level_grid = [
            "############################",
            "#............##............#",
            "#.#........#.##.#........#.#",
            "#.#........#.##.#........#.#",
            "#.####..####.##.####..####.#",
            "#............P.............#",
            "#......##..######..##......#",
            "#......##....##....##......#",
            "####...##... ## ...##...####",
            "   #...#    GGGG    #...#   ",
            "####...#  ########  #...####",
            "#............##............#",
            "#............##............#",
            "#...##................##...#",
            "###.##.##.########.##.##.###",
            "#......##....##....##......#",
            "#......##....##....##......#",
            "#..........................#",
            "############################",
        ]

        self.cell_size = 1.0
        self.width = len(self.level_grid[0])
        self.height = len(self.level_grid)
        self.max_dist = math.hypot(self.width, self.height)

        self.dt = 0.2
        self.max_linear_speed = 2.0
        self.max_angular_speed = 2.5
        self._ray_step = 0.2
        self._lidar_angles = tuple(i * (math.pi / 4.0) for i in range(8))

        self._wall_grid = [[cell == "#" for cell in row] for row in self.level_grid]

        self._build_world()

    def _build_world(self) -> None:
        self.env = Environnement(largeur=self.width, hauteur=self.height)
        creer_carte(self.env, self.level_grid, taille_case=self.cell_size)

        px, py = self.env.pacman_spawn
        moteur = MoteurOmnidirectionnel(vx=0.0, vy=0.0, omega=0.0)
        self.pacman = Pacman(
            x=px,
            y=py,
            orientation=0.0,
            moteur=moteur,
            rayon=0.25,
        )
        self.pacman.score = 0
        self.env.ajouter_robot(self.pacman)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._build_world()
        self.step_count = 0
        self._stagnant_steps = 0
        self._last_position = (self.pacman.x, self.pacman.y)

        return self._get_obs(), {}

    def render(self):
        pass

    def _norm01_to_m11(self, value: float) -> float:
        value = max(0.0, min(1.0, float(value)))
        return 2.0 * value - 1.0

    def _cell_rect(self, row: int, col: int) -> tuple[float, float, float, float]:
        x0 = col * self.cell_size
        x1 = x0 + self.cell_size
        y0 = (self.height - row - 1) * self.cell_size
        y1 = y0 + self.cell_size
        return x0, x1, y0, y1

    def _circle_intersects_wall_cell(self, x: float, y: float, rayon: float, row: int, col: int) -> bool:
        x0, x1, y0, y1 = self._cell_rect(row, col)
        closest_x = min(max(x, x0), x1)
        closest_y = min(max(y, y0), y1)
        dx = x - closest_x
        dy = y - closest_y
        return dx * dx + dy * dy <= rayon * rayon

    def _hits_wall(self, x: float, y: float, rayon: float | None = None) -> bool:
        if rayon is None:
            rayon = self.pacman.rayon

        min_col = max(0, int((x - rayon) / self.cell_size))
        max_col = min(self.width - 1, int((x + rayon) / self.cell_size))
        min_row = max(0, self.height - 1 - int((y + rayon) / self.cell_size))
        max_row = min(self.height - 1, self.height - 1 - int((y - rayon) / self.cell_size))

        for row in range(min_row, max_row + 1):
            wall_row = self._wall_grid[row]
            for col in range(min_col, max_col + 1):
                if wall_row[col] and self._circle_intersects_wall_cell(x, y, rayon, row, col):
                    return True

        return False

    def _nearest_pellet(self):
        if not self.env.points:
            return None, float("inf")

        best = None
        best_dist = float("inf")
        for x, y in self.env.points:
            dist = math.dist((self.pacman.x, self.pacman.y), (x, y))
            if dist < best_dist:
                best = (x, y)
                best_dist = dist
        return best, best_dist

    def _world_to_robot_frame(self, dx: float, dy: float) -> tuple[float, float]:
        theta = self.pacman.orientation
        forward = dx * math.cos(theta) + dy * math.sin(theta)
        lateral = -dx * math.sin(theta) + dy * math.cos(theta)
        return forward, lateral

    def _ray_distance(self, angle_offset: float) -> float:
        angle = self.pacman.orientation + angle_offset
        dx = math.cos(angle)
        dy = math.sin(angle)
        dist = 0.0

        while dist < self.max_dist:
            dist += self._ray_step
            x = self.pacman.x + dx * dist
            y = self.pacman.y + dy * dist

            if x < 0 or x > self.width or y < 0 or y > self.height:
                break
            if self._hits_wall(x, y):
                break

        return self._norm01_to_m11(dist / self.max_dist)

    def _lidar_scan(self) -> list[float]:
        return [self._ray_distance(angle) for angle in self._lidar_angles]

    def _get_obs(self):
        lidar_scan = self._lidar_scan()
        x_norm = self._norm01_to_m11(self.pacman.x / max(1e-6, self.width))
        y_norm = self._norm01_to_m11(self.pacman.y / max(1e-6, self.height))
        cos_t = math.cos(self.pacman.orientation)
        sin_t = math.sin(self.pacman.orientation)

        pellet, pellet_dist = self._nearest_pellet()
        if pellet is None:
            pellet_forward = 0.0
            pellet_lateral = 0.0
            pellet_dist_norm = 1.0
        else:
            dx = pellet[0] - self.pacman.x
            dy = pellet[1] - self.pacman.y
            forward, lateral = self._world_to_robot_frame(dx, dy)
            pellet_forward = forward / max(1e-6, self.width)
            pellet_lateral = lateral / max(1e-6, self.height)
            pellet_dist_norm = self._norm01_to_m11(pellet_dist / self.max_dist)

        remaining_frac = len(self.env.points) / max(1, self.width * self.height)
        remaining_norm = self._norm01_to_m11(remaining_frac)
        score_norm = self._norm01_to_m11(self.pacman.score / 100.0)

        return np.array(
            [
                *lidar_scan,
                x_norm,
                y_norm,
                cos_t,
                sin_t,
                pellet_forward,
                pellet_lateral,
                pellet_dist_norm,
                remaining_norm,
                score_norm,
            ],
            dtype=np.float32,
        )

    def step(self, action):
        self.step_count += 1

        action = np.asarray(action, dtype=np.float32).reshape(3)
        action = np.clip(action, -1.0, 1.0)

        dist_before = self._nearest_pellet()[1]
        old_x = self.pacman.x
        old_y = self.pacman.y

        vx_cmd = float(action[0]) * self.max_linear_speed
        vy_cmd = float(action[1]) * self.max_linear_speed
        omega_cmd = float(action[2]) * self.max_angular_speed

        self.pacman.commander(vx_cmd, vy_cmd, omega_cmd)
        self.pacman.mettre_a_jour(self.dt)

        reward = -0.01

        if self._hits_wall(self.pacman.x, self.pacman.y, self.pacman.rayon):
            self.pacman.x = old_x
            self.pacman.y = old_y
            # On garde la rotation, mais on annule une orientation devenue numeriquement trop large.
            self.pacman.orientation = ((self.pacman.orientation + math.pi) % (2 * math.pi)) - math.pi
            reward -= 0.25
        else:
            movement = math.dist((old_x, old_y), (self.pacman.x, self.pacman.y))
            if movement < 0.02:
                reward -= 0.03

        self.env.limiter_positions(self.pacman)

        collected = self.pacman.ramasser_points(self.env)
        reward += collected * 1.0

        dist_after = self._nearest_pellet()[1]
        if math.isfinite(dist_before) and math.isfinite(dist_after):
            reward += 0.1 * (dist_before - dist_after)

        current_position = (self.pacman.x, self.pacman.y)
        if math.dist(current_position, self._last_position) < 0.02:
            self._stagnant_steps += 1
        else:
            self._stagnant_steps = 0
        self._last_position = current_position

        if self._stagnant_steps >= 8:
            reward -= 0.08

        terminated = False
        truncated = False

        if not self.env.points:
            reward += 10.0
            terminated = True

        if self.max_steps is not None and self.step_count >= self.max_steps:
            truncated = True

        info = {
            "vx_cmd": vx_cmd,
            "vy_cmd": vy_cmd,
            "omega_cmd": omega_cmd,
            "collision": self._hits_wall(self.pacman.x, self.pacman.y, self.pacman.rayon),
        }
        return self._get_obs(), reward, terminated, truncated, info
