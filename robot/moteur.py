from abc import ABC, abstractmethod
from math import cos, sin

class Moteur(ABC):

    @abstractmethod
    def commander(self, *args, **kwargs):
        pass

    @abstractmethod
    def mettre_a_jour(self, robot, dt):
        pass

