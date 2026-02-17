import pygame
from abc import ABC, abstractmethod


class Controleur(ABC):

    @abstractmethod
    def lire_commande(self):
        pass


class ControleurTerminal(Controleur):

    def lire_commande(self):
        print("Commande differentiel : v omega (ex: 1.0 0.5)")
        entree = input("> ")

        try:
            v, omega = map(float, entree.split())
        except:
            v, omega = 0.0, 0.0

        return {"v": v, "omega": omega}
        

class ControleurClavierPygame(Controleur):

    def lire_commande(self):

        v = 0.0
        omega = 0.0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            v = 1.0
        if keys[pygame.K_DOWN]:
            v = -1.0
        if keys[pygame.K_LEFT]:
            omega = 1.0
        if keys[pygame.K_RIGHT]:
            omega = -1.0

        return {"v": v, "omega":omega}