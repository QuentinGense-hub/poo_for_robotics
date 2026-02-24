from robot.robot_mobile import RobotMobile
from robot.moteur import MoteurDifferentiel


class Pacman(RobotMobile):

    def __init__(self, x, y):
        moteur = MoteurDifferentiel(v=0.0, omega=0.0)
        super().__init__(x, y, orientation=0.0, moteur=moteur, rayon=0.4)

        self.score = 0
        self.power_mode = False
        self.power_timer = 0

        # Parametres physiques
        self.vitesse_max = 3.0
        self.vitesse_rotation = 4.0

    # Commandes joueur / IA
    def avancer(self):
        self.moteur.commander(v=self.vitesse_max, omega=0)

    def tourner_gauche(self):
        self.moteur.commander(v=self.vitesse_max, omega=-self.vitesse_rotation)

    def tourner_droite(self):
        self.moteur.commander(v=self.vitesse_max, omega=-self.vitesse_rotation)

    def arreter(self):
        self.moteur.commander(v=0, omega=0)

    # Update
    def update(self, dt):
        self.mettre_a_jour(dt)