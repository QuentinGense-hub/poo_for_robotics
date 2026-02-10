from abc import ABC, abstractmethod
from math import cos, sin

class Moteur(ABC):

    @abstractmethod
    def commander(self, *args, **kwargs):
        pass

    @abstractmethod
    def mettre_a_jour(self, robot, dt):
        pass

class MoteurDifferentiel(Moteur):
    def __init__(self, v=0.0, omega=0.0):
        self.v = v
        self.omega = omega

    def commander(self, v, omega):
        self.v = v
        self.omega = omega

    def mettre_a_jour(self, robot, dt):
        robot.orientation += self.omega * dt
        robot.x += self.v * cos(robot.orientation) * dt
        robot.y += self.v * sin(robot.orientation) * dt

