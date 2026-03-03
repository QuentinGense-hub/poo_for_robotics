import math
from robot.robot_mobile import RobotMobile

class Ghost(RobotMobile):
    def __init__(self, *args, max_speed=0.8, max_omega=2.0, **kwargs):
        # on crée un moteur différentiel si besoin
        from robot.moteur import MoteurDifferentiel
        moteur = kwargs.pop("moteur", MoteurDifferentiel(v=0.0, omega=0.0, vmax=max_speed, omegamax=max_omega))
        super().__init__(*args, moteur=moteur, **kwargs)
        self.max_speed = max_speed
        self.max_omega = max_omega
        self.nom = "Ghost"

    def ia_poursuite(self, pacman, dt):
        """
Simple stratégie : viser l'angle vers Pacman, tourner proportionnellement,
avancer proportionnellement à l'angle (plus l'angle est petit -> plus il avance).
        """
        dx = pacman.x - self.x
        dy = pacman.y - self.y
        cible_angle = math.atan2(dy, dx)
        # plus petit écart angulaire dans [-pi, pi]
        diff = (cible_angle - self.orientation + math.pi) % (2*math.pi) - math.pi

        # paramètres simples
        Kp_ang = 3.0  # gain proportionnel sur l'angle
        omega_cmd = max(-self.max_omega, min(self.max_omega, Kp_ang * diff))

        # vitesse avant : réduite si l'angle est grand
        # cos(diff) varie de -1 à 1 ; on garde que la partie positive
        forward = self.max_speed * max(0.0, math.cos(diff))

        # commander le moteur (différentiel)
        self.commander(forward, omega_cmd)