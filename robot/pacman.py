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