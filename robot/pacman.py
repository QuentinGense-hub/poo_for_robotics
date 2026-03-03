import math
from robot.robot_mobile import RobotMobile

class Pacman(RobotMobile):
    def __init__(self, *args, rayon=0.25, **kwargs):
        super().__init__(*args, rayon=rayon, **kwargs)
        self.score = 0
        self.nom = "Pacman"

    def ramasser_points(self, environnement):
        """
Parcourt les points (dots) dans l'environnement et ramasse
ceux dans le rayon du pacman.
        """
        to_remove = []
        for p in environnement.points:
            dx = p[0] - self.x
            dy = p[1] - self.y
            if dx*dx + dy*dy <= (self.rayon + 0.05)**2:
                to_remove.append(p)
        for p in to_remove:
            environnement.points.remove(p)
            self.score += 10  # valeur d'un dot
        return len(to_remove)

    def ia_simple(self, env):
        if not env.points:
            self.commander(0, 0)
            return

        # cible = point le plus proche
        cible = min(env.points,
                    key=lambda p: (p[0]-self.x)**2 + (p[1]-self.y)**2)

        meilleur_angle = None
        meilleur_score = float("inf")

        # tester plusieurs directions autour
        for delta in [i * 0.3 for i in range(-6, 7)]:
            angle = self.orientation + delta

            test_x = self.x + 0.3 * math.cos(angle)
            test_y = self.y + 0.3 * math.sin(angle)

            # simuler position temporaire
            old_x, old_y = self.x, self.y
            self.x, self.y = test_x, test_y

            collision = env.collision_obstacles(self)

            self.x, self.y = old_x, old_y

            if collision:
                continue

            score = (cible[0]-test_x)**2 + (cible[1]-test_y)**2

            if score < meilleur_score:
                meilleur_score = score
                meilleur_angle = angle

        if meilleur_angle is None:
            self.commander(0, 2.0)
            return

        diff = (meilleur_angle - self.orientation + math.pi) % (2*math.pi) - math.pi

        omega = 3.0 * diff
        vitesse = 1.0 * max(0, math.cos(diff))

        self.commander(vitesse, omega)