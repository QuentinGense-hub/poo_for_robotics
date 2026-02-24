import pygame
from robot.robot_mobile import RobotMobile
from robot.moteur import MoteurDifferentiel
from robot.controleur import ControleurClavierPygame
from robot.vue import VuePygame
from robot.environnement import Environnement
from robot.obstacle import ObstacleCirculaire, ObstacleRectangulaire


robot = RobotMobile(moteur=MoteurDifferentiel())
env = Environnement(largeur=10, hauteur=8)

env.ajouter_robot(robot)

env.ajouter_obstacle(ObstacleCirculaire(2, 2, 0.5))
env.ajouter_obstacle(ObstacleCirculaire(-2, -1, 0.7))
env.ajouter_obstacle(ObstacleRectangulaire(0, -2, 3, 1))

controleur = ControleurClavierPygame()
vue = VuePygame()

dt = 0.05
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    commande = controleur.lire_commande()
    robot.commander(**commande)

    env.mettre_a_jour(dt)

    vue.dessiner_environnement(env)
    vue.tick(60)

pygame.quit()
