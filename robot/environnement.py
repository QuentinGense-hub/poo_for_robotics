import math

class Environnement:

    def __init__(self, largeur=10, hauteur=10):
        self.largeur = largeur
        self.hauteur = hauteur
        self.robot = None
        self.ghosts = []
        self.obstacles = []
        self.points = []  # liste de tuples (x,y) pour les dots

    def ajouter_robot(self, robot):
        self.robot = robot

    def ajouter_ghost(self, ghost):
        self.ghosts.append(ghost)

    def ajouter_obstacle(self, obstacle):
        self.obstacles.append(obstacle)

    def ajouter_point(self, x, y):
        self.points.append((x, y))

    def limiter_positions(self, robot):
        # empêche de sortir des limites du monde centré en (0,0)
        demi_largeur = self.largeur / 2.0
        demi_hauteur = self.hauteur / 2.0
        if robot.x - robot.rayon < -demi_largeur:
            robot.x = -demi_largeur + robot.rayon
        if robot.x + robot.rayon > demi_largeur:
            robot.x = demi_largeur - robot.rayon
        if robot.y - robot.rayon < -demi_hauteur:
            robot.y = -demi_hauteur + robot.rayon
        if robot.y + robot.rayon > demi_hauteur:
            robot.y = demi_hauteur - robot.rayon

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
            self.robot.mettre_a_jour(dt)
            # si collision : revenir en arrière et stopper
            if self.collision_obstacles(self.robot):
                self.robot.x, self.robot.y, self.robot.orientation = x_old, y_old, theta_old
                # si moteur différentiel : couper la vitesse
                try:
                    self.robot.moteur.commander(0.0, 0.0)
                except Exception:
                    pass
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
                    g.ia_poursuite(self.robot, dt)
            except Exception:
                pass
            xg_old, yg_old, theg_old = g.x, g.y, g.orientation
            g.mettre_a_jour(dt)
            if self.collision_obstacles(g):
                # simple réaction : revenir en arrière et arrêter
                g.x, g.y, g.orientation = xg_old, yg_old, theg_old
                try:
                    g.moteur.commander(0.0, 0.0)
                except Exception:
                    pass
            self.limiter_positions(g)