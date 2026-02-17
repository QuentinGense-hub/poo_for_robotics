from abc import ABC, abstractmethod
import math

class Obstacle(ABC):

    @abstractmethod
    def collision(self, robot):
        pass

    @abstractmethod
    def dessiner(self, vue):
        pass


class ObstacleCirculaire(Obstacle):

    def __init__(self, x, y, rayon):
        self._x = x
        self._y = _y
        self._rayon = rayon

    def collision(self, robot):

        dx = robot.x - self._x
        dy = robot.y - self._y

        distance = math.sqrt(dx**2 + dy**2)

        return distance <= (self._rayon + robot.rayon)

    def dessiner(self, vue):
        px, py = vue.convertir_coordonnees(self._x, self._y)
        r = int(self._rayon * vue.scale)

        import pygame
        pygame.draw.circle(vue.screen, (0, 0, 0), (px, py), r)