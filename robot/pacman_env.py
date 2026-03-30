import gymnasium as gym
from gymnasium import spaces
import numpy as np
import math
from robot.environnement import Environnement
from robot.pacman import Pacman
from robot.map_loader import creer_carte
from gymnasium.envs.registration import register

class PacmanEnv(gym.Env):

    register(
        id="PacmanPPO-v0",
        entry_point="robot.pacman_env:PacmanEnv",
    )

    def __init__(self):
        super().__init__()

        # 0: stay
        # 1: up
        # 2: down
        # 3: left
        # 4: right
        self.action_space = spaces.Discrete(5)

        # On commencera simple : position x,y + score
        self.observation_space = spaces.Box(
            low=-1.0,
            high=1.0,
            shape=(10,),
            dtype=np.float32
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
            "############################"
        ]

        self.cell_size = 1.0
        self.width = len(self.level_grid[0])
        self.height = len(self.level_grid)
        self.max_dist = math.hypot(self.width, self.height)
        self._move_step = 0.2
        self._moves = (
            (0.0, 0.0),
            (0.0, self._move_step),
            (0.0, -self._move_step),
            (-self._move_step, 0.0),
            (self._move_step, 0.0),
        )
        self._wall_grid = [
            [cell == "#" for cell in row]
            for row in self.level_grid
        ]

        self._build_world()

    def _build_world(self):
        self.env = Environnement(
            largeur=self.width,
            hauteur=self.height
        )

        creer_carte(self.env, self.level_grid, taille_case=self.cell_size)

        px, py = self.env.pacman_spawn

        self.pacman = Pacman(
            x=px,
            y=py,
            moteur=None,
            rayon=0.25
        )

        self.pacman.score = 0
        self.env.ajouter_robot(self.pacman)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self._build_world()
        self.step_count = 0

        observation = self._get_obs()
        info = {}

        return observation, info

    def _get_obs(self):
        # Distances de rayons dans les 4 directions cardinales
        ray_up = self._ray_distance(0.0, 1.0)
        ray_right = self._ray_distance(1.0, 0.0)
        ray_down = self._ray_distance(0.0, -1.0)
        ray_left = self._ray_distance(-1.0, 0.0)

        x_norm = self._norm01_to_m11(self.pacman.x / max(1e-6, self.width))
        y_norm = self._norm01_to_m11(self.pacman.y / max(1e-6, self.height))

        theta = getattr(self.pacman, "orientation", 0.0)
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)

        remaining_frac = len(self.env.points) / max(1, self.width * self.height)
        remaining_norm = self._norm01_to_m11(remaining_frac)

        score_norm = self._norm01_to_m11(self.pacman.score / 100.0)

        obs = np.array([
            x_norm,
            y_norm,
            cos_t,
            sin_t,
            ray_up,
            ray_right,
            ray_down,
            ray_left,
            remaining_norm,
            score_norm,
        ], dtype=np.float32)

        return obs

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

    def _normalize_delta(self, dx: float, dy: float) -> tuple[float, float]:
        return dx / max(1e-6, self.width), dy / max(1e-6, self.height)

    def _nearest_pellet(self):
        if not self.env.points:
            return None, float("inf")

        best = None
        best_dist = float("inf")

        for x, y in self.env.points:
            d = math.dist((self.pacman.x, self.pacman.y), (x, y))
            if d < best_dist:
                best = (x, y)
                best_dist = d

        return best, best_dist

    def _nearest_ghost(self):
        if not hasattr(self.env, "ghosts") or not self.env.ghosts:
            return None, float("inf")

        best = None
        best_dist = float("inf")

        for g in self.env.ghosts:
            d = math.dist((self.pacman.x, self.pacman.y), (g.x, g.y))
            if d < best_dist:
                best = (g.x, g.y)
                best_dist = d

        return best, best_dist

    def _ray_distance(self, dx: float, dy: float, step: float = 0.10) -> float:
        """
    Raycast simple: on avance petit à petit jusqu'à toucher un mur
    ou sortir de la carte.
    Retourne une valeur normalisée dans [-1, 1].
        """
        dist = 0.0

        while dist < self.max_dist:
            dist += step
            x = self.pacman.x + dx * dist
            y = self.pacman.y + dy * dist

            # Hors carte
            if x < 0 or x > self.width or y < 0 or y > self.height:
                break

            if self._hits_wall(x, y):
                break

        return self._norm01_to_m11(dist / self.max_dist)

    def _front_is_wall(self) -> float:
        """
    1.0 si un mur est juste devant, -1.0 sinon.
    On prend la direction dominante de l'orientation actuelle.
        """
        theta = getattr(self.pacman, "orientation", 0.0)
        c = math.cos(theta)
        s = math.sin(theta)

        if abs(c) >= abs(s):
            dx = 1.0 if c >= 0 else -1.0
            dy = 0.0
        else:
            dx = 0.0
            dy = 1.0 if s >= 0 else -1.0

        # On regarde à une petite distance devant
        forward_x = self.pacman.x + dx * self._move_step
        forward_y = self.pacman.y + dy * self._move_step

        hit = (
            forward_x < 0 or forward_x > self.width or
            forward_y < 0 or forward_y > self.height or
            self._hits_wall(forward_x, forward_y)
        )

        return 1.0 if hit else -1.0

    def _best_pellet_direction(self):
        """
    Direction optimale vers la pastille la plus proche.
    Retourne :
    - one-hot de la meilleure action (up, right, down, left)
    - dx, dy normalisés vers la pastille
    - distance normalisée vers la pastille
        """
        pellet, dist = self._nearest_pellet()

        if pellet is None:
            return [0.0, 0.0, 0.0, 0.0], 0.0, 0.0, 1.0

        dx = pellet[0] - self.pacman.x
        dy = pellet[1] - self.pacman.y

        # Choix cardinal simple : axe dominant
        one_hot = [0.0, 0.0, 0.0, 0.0]  # up, right, down, left
        if abs(dx) >= abs(dy):
            one_hot[1 if dx > 0 else 3] = 1.0
        else:
            one_hot[0 if dy > 0 else 2] = 1.0

        ndx, ndy = self._normalize_delta(dx, dy)
        ndist = self._norm01_to_m11(dist / self.max_dist)

        return one_hot, ndx, ndy, ndist

    def _wall_clearances(self):
        left = max(0.0, self.pacman.x)
        right = max(0.0, self.width - self.pacman.x)
        bottom = max(0.0, self.pacman.y)
        top = max(0.0, self.height - self.pacman.y)
        return left, right, bottom, top

    def step(self, action):
        self.step_count += 1
        dx, dy = self._moves[action]

        old_x, old_y = self.pacman.x, self.pacman.y

        self.pacman.x += dx
        self.pacman.y += dy

        # Collision murs
        if self._hits_wall(self.pacman.x, self.pacman.y, self.pacman.rayon):
            self.pacman.x, self.pacman.y = old_x, old_y
            reward = -0.2
        else:
            reward = -0.01

        # Ramassage points
        collected = self.pacman.ramasser_points(self.env)
        reward += collected * 1.0

        terminated = False
        truncated = False

        if not self.env.points:
            reward += 10
            terminated = True

        if self.step_count > 500:
            truncated = True

        observation = self._get_obs()

        return observation, reward, terminated, truncated, {}
