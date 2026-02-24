# robot/pacman.py
from robot.robot_mobile import RobotMobile
from robot.moteur import MoteurDifferentiel

class Pacman(RobotMobile):
    def __init__(self, x=0.0, y=0.0, orientation=0.0, rayon=0.35, vitesse_max=2.5):
        # Crée un moteur différentiel par défaut ; on garde l'API existante
        moteur = MoteurDifferentiel(v=0.0, omega=0.0)
        super().__init__(x=x, y=y, orientation=orientation, moteur=moteur, rayon=rayon)

        self.score = 0
        self.power_mode = False
        self.power_timer = 0.0

        self.vitesse_max = vitesse_max
        self.vitesse_rotation = 3.0  # rad/s (valeur indicative)

    # commandes simples — elles appellent le moteur via RobotMobile.commander si disponible
    def avancer(self):
        # on suppose que RobotMobile a une méthode commander(v, omega) ou on passe par self.moteur.commander
        if hasattr(self, "commander"):
            try:
                self.commander(v=self.vitesse_max, omega=0.0)
                return
            except Exception:
                pass
        # fallback direct sur le moteur si nécessaire
        if hasattr(self, "moteur") and hasattr(self.moteur, "commander"):
            self.moteur.commander(self.vitesse_max, 0.0)

    def tourner_gauche(self):
        if hasattr(self, "commander"):
            try:
                self.commander(v=self.vitesse_max, omega=-self.vitesse_rotation)
                return
            except Exception:
                pass
        if hasattr(self, "moteur") and hasattr(self.moteur, "commander"):
            self.moteur.commander(self.vitesse_max, -self.vitesse_rotation)

    def tourner_droite(self):
        if hasattr(self, "commander"):
            try:
                self.commander(v=self.vitesse_max, omega=self.vitesse_rotation)
                return
            except Exception:
                pass
        if hasattr(self, "moteur") and hasattr(self.moteur, "commander"):
            self.moteur.commander(self.vitesse_max, self.vitesse_rotation)

    def arreter(self):
        if hasattr(self, "commander"):
            try:
                self.commander(v=0.0, omega=0.0)
                return
            except Exception:
                pass
        if hasattr(self, "moteur") and hasattr(self.moteur, "commander"):
            try:
                # some motors expect (v, omega)
                self.moteur.commander(0.0, 0.0)
            except Exception:
                # try other signature
                try:
                    self.moteur.commander(v=0.0, omega=0.0)
                except Exception:
                    pass

    def update(self, dt):
        # décroissant power timer si actif
        if self.power_mode:
            self.power_timer -= dt
            if self.power_timer <= 0.0:
                self.power_mode = False
                self.power_timer = 0.0

        # déléguer la mise à jour moteur/position au parent si la méthode existe
        if hasattr(self, "mettre_a_jour"):
            try:
                self.mettre_a_jour(dt)
            except Exception:
                # fallback: tenter d'appeler le moteur directement
                if hasattr(self, "moteur") and hasattr(self.moteur, "mettre_a_jour"):
                    try:
                        self.moteur.mettre_a_jour(self, dt)
                    except Exception:
                        pass