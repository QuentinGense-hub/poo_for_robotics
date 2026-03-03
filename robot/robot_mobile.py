import math
from robot.moteur import Moteur

class RobotMobile:
    _nb_robots = 0

    def __init__(self, x=0.0, y=0.0, orientation=0.0, moteur: Moteur=None, rayon=0.3, nom="robot"):
        self.__x = float(x)
        self.__y = float(y)
        self.__orientation = float(orientation)  # en radians
        self.__rayon = float(rayon)
        self.nom = nom

        if moteur is not None and not RobotMobile.moteur_valide(moteur):
            raise TypeError("Le moteur fourni n'est pas valide")

        self.moteur = moteur
        RobotMobile._nb_robots += 1

    # propriétés d'accès
    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, v):
        self.__x = float(v)

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, v):
        self.__y = float(v)

    @property
    def orientation(self):
        return self.__orientation

    @orientation.setter
    def orientation(self, v):
        self.__orientation = float(v)

    @property
    def rayon(self):
        return self.__rayon

    def commander(self, *args, **kwargs):
        """
Déporte la commande vers le moteur
Par ex. pour un moteur différentiel : commander(v, omega)
        """
        if self.moteur is None:
            return
        self.moteur.commander(*args, **kwargs)

    def mettre_a_jour(self, dt):
        """
Appel du moteur pour appliquer la commande (modifie x,y,orientation)
        """
        if self.moteur:
            self.moteur.mettre_a_jour(self, dt)

    def __str__(self):
        return f"{self.nom} (x={self.x:.2f}, y={self.y:.2f}, theta={self.orientation:.2f})"

    @classmethod
    def nombre_robots(cls):
        return cls._nb_robots

    @staticmethod
    def moteur_valide(moteur):
        from robot.moteur import Moteur
        return isinstance(moteur, Moteur)