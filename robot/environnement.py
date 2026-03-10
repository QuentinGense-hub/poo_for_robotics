import math

class Environnement:

    def __init__(self, largeur=10, hauteur=10):
        self.largeur = largeur
        self.hauteur = hauteur
        self.robot = None
        self.ghosts = []
        self.obstacles = []
        self.points = []  # liste de tuples (x,y) pour les dots
        self.ghost_spawns = []
        self.pacman_spawn = None

    def ajouter_robot(self, robot):
        self.robot = robot

    def ajouter_ghost(self, ghost):
        self.ghosts.append(ghost)

    def ajouter_obstacle(self, obstacle):
        self.obstacles.append(obstacle)

    def ajouter_point(self, x, y):
        self.points.append((x, y))

    def limiter_positions(self, robot):
        if robot.x - robot.rayon < 0:
            robot.x = robot.rayon
        if robot.x + robot.rayon > self.largeur:
            robot.x = self.largeur - robot.rayon

        if robot.y - robot.rayon < 0:
            robot.y = robot.rayon
        if robot.y + robot.rayon > self.hauteur:
            robot.y = self.hauteur - robot.rayon

    def collision_obstacles(self, robot):
        # parcours des obstacles, retourne True si collision détectée
        for obs in self.obstacles:
            try:
                if obs.collision(robot):
                    return True
            except Exception:
                # si un obstacle n'implémente pas collision proprement, on ignore
                pass
        return False

    def mettre_a_jour(self, dt):
        # Mettre à jour le robot principal
        if self.robot:
            x_old, y_old, theta_old = self.robot.x, self.robot.y, self.robot.orientation
            try:
                self.robot.ia_simple(self)
            except Exception:
                pass
            self.robot.mettre_a_jour(dt)
            # si collision : revenir en arrière et stopper
            if self.collision_obstacles(self.robot):
                # on annule seulement la position
                self.robot.x, self.robot.y = x_old, y_old
                # on garde la nouvelle orientation
            else:
                # ramasser points uniquement si pas collision
                try:
                    self.robot.ramasser_points(self)
                except Exception:
                    pass
            self.limiter_positions(self.robot)

        # ghosts : IA puis mise à jour
        for g in list(self.ghosts):
            try:
                # si pacman présent, appeler l'IA
                if self.robot:
                    g.ia_poursuite(self.robot, self)
            except Exception:
                pass
            xg_old, yg_old, theg_old = g.x, g.y, g.orientation
            g.mettre_a_jour(dt)
            if self.collision_obstacles(g):
                g.x, g.y = xg_old, yg_old
            self.limiter_positions(g)

    def ajouter_ghost_spawn(self, x, y):
        """Ajoute une position de spawn (utile si on veut ajouter dynamiquement)."""
        self.ghost_spawns.append((x, y))

    def lister_ghost_spawns(self):
        return list(self.ghost_spawns)

    def spawn_ghosts(self, ghost_class=None, per_spawn=1):
        """
Instancie des Ghosts aux positions de spawn.
ghost_class: la classe à instancier (par défaut Robot Ghost du module).
per_spawn: combien de fantomes créer par spawn (1 par défaut).
        """
        if ghost_class is None:
            from robot.ghost import Ghost as _Ghost
            ghost_class = _Ghost

        import math
        for (x, y) in self.ghost_spawns:
            for n in range(per_spawn):
                # petits offsets si per_spawn > 1 pour les séparer légèrement
                offx = (n - (per_spawn-1)/2) * 0.2 * 0.9
                orientation = math.pi  # par défaut orientés vers la gauche
                g = ghost_class(x + offx, y, orientation=orientation)
                self.ajouter_ghost(g)