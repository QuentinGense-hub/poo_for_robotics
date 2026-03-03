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

    def ia_poursuite(self, pacman, env):

        meilleur_angle = None
        meilleur_score = float("inf")

        # Échantillonnage angulaire autour de la direction actuelle
        for delta in [i * 0.3 for i in range(-6, 7)]:
            angle = self.orientation + delta

            # Petit pas de simulation
            test_x = self.x + 0.35 * math.cos(angle)
            test_y = self.y + 0.35 * math.sin(angle)

            # Sauvegarde position
            old_x, old_y = self.x, self.y
            self.x, self.y = test_x, test_y

            collision = env.collision_obstacles(self)

            # Restaurer
            self.x, self.y = old_x, old_y

            if collision:
                continue

            # Distance au pacman
            score = (pacman.x - test_x)**2 + (pacman.y - test_y)**2

            if score < meilleur_score:
                meilleur_score = score
                meilleur_angle = angle

        # Si toutes directions bloquées → tourner sur place
        if meilleur_angle is None:
            self.commander(0, 2.5)
            return

        # Calcul rotation progressive
        diff = (meilleur_angle - self.orientation + math.pi) % (2*math.pi) - math.pi

        omega = 3.0 * diff
        vitesse = self.max_speed * max(0.0, math.cos(diff))

        self.commander(vitesse, omega)