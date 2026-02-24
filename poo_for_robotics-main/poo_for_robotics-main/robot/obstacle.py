from abc import ABC, abstractmethod
import math
import pygame

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
        self._y = y
        self._rayon = rayon

    def collision(self, robot):

        dx = robot.x - self._x
        dy = robot.y - self._y

        distance = math.sqrt(dx**2 + dy**2)

        return distance <= (self._rayon + robot.rayon)

    def dessiner(self, vue):
        px, py = vue.convertir_coordonnees(self._x, self._y)
        r = int(self._rayon * vue.scale)

        pygame.draw.circle(vue.screen, (255, 0, 0), (px, py), r)


class ObstacleRectangulaire(Obstacle):

    def __init__(self, x, y, largeur, hauteur):
        self._x = x
        self._y = y
        self._largeur = largeur
        self._hauteur = hauteur

    def collision(self, robot):

        # Clamp du centre robot dans le rectangle
        demi_l = self._largeur / 2
        demi_h = self._hauteur / 2

        plus_proche_x = max(self._x - demi_l,
                            min(robot.x, self._x + demi_l))

        plus_proche_y = max(self._y - demi_h,
                            min(robot.y, self._y + demi_h))

        dx = robot.x - plus_proche_x
        dy = robot.y - plus_proche_y

        return (dx**2 + dy**2) <=robot.rayon**2

    def dessiner(self, vue):

        px, py = vue.convertir_coordonnees(self._x, self._y)

        largeur_px = int(self._largeur * vue.scale)
        hauteur_px = int(self._hauteur * vue.scale)

        rect = pygame.Rect(0, 0, largeur_px, hauteur_px)
        rect.center = (px, py)

        pygame.draw.rect(vue.screen, (50, 50, 50), rect)