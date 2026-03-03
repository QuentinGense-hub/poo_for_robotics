from abc import ABC, abstractmethod
from math import cos, sin, pi

class Moteur(ABC):

    @abstractmethod
    def commander(self, *args, **kwargs):
        pass

    @abstractmethod
    def mettre_a_jour(self, robot, dt):
        pass

class MoteurDifferentiel(Moteur):
    """
Moteur différentiel simple : commande (v, omega)
v : vitesse avant (m/s)
omega : vitesse angulaire (rad/s)
    """
    def __init__(self, v=0.0, omega=0.0, vmax=1.0, omegamax=3.0):
        self.v = float(v)
        self.omega = float(omega)
        self.vmax = float(vmax)
        self.omegamax = float(omegamax)

    def commander(self, v, omega):
        # saturation des commandes
        if v > self.vmax: v = self.vmax
        if v < -self.vmax: v = -self.vmax
        if omega > self.omegamax: omega = self.omegamax
        if omega < -self.omegamax: omega = -self.omegamax
        self.v = float(v)
        self.omega = float(omega)

    def mettre_a_jour(self, robot, dt):
        # intégration simple des équations cinématiques
        theta = robot.orientation
        dx = self.v * cos(theta) * dt
        dy = self.v * sin(theta) * dt
        dtheta = self.omega * dt

        robot.x += dx
        robot.y += dy
        # normaliser l'orientation dans [-pi, pi]
        robot.orientation = ((robot.orientation + dtheta + pi) % (2*pi)) - pi

class MoteurOmnidirectionnel(Moteur):
    """
Exemple d’omni : commandes vx, vy (dans le repère du robot), omega
    """
    def __init__(self, vx=0.0, vy=0.0, omega=0.0):
        self.vx = vx
        self.vy = vy
        self.omega = omega

    def commander(self, vx, vy, omega):
        self.vx = vx
        self.vy = vy
        self.omega = omega

    def mettre_a_jour(self, robot, dt):
        from math import cos, sin
        robot.x += (self.vx * cos(robot.orientation) - self.vy * sin(robot.orientation)) * dt
        robot.y += (self.vx * sin(robot.orientation) + self.vy * cos(robot.orientation)) * dt
        robot.orientation += self.omega * dt