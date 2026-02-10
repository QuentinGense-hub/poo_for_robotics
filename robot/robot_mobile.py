import math
from robot.moteur import Moteur

class RobotMobile:
    _nb_robots = 0 # attribut statique

    def __init__(self, x=0.0, y=0.0, orientation=0.0, moteur=None):
        self.__x = x
        self.__y = y
        self.__orientation = orientation

        if moteur is not None and not RobotMobile.moteur_valide(moteur):
            raise TypeError("Le moteur fourni n'est pas valide")

        self.moteur = moteur
        RobotMobile._nb_robots += 1