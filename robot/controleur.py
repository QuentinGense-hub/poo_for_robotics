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
        