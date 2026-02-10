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

    #Encapsulation
    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = float(value)

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = float(value)

    @property
    def orientation(self):
        return self.__orientation

    @orientation.setter
    def orientation(self, value):
        self.__orientation = value % (2 * math.pi)

    #Méthodes de base
    def avancer(self, distance):
        self.__x += distance * math.cos(self.__orientation)
        self.__y += distance * math.sin(self.__orientation)

    def tourner(self, angle):
        self.orientation += angle