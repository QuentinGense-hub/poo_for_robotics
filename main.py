import pygame
from robot.robot_mobile import RobotMobile
from robot.moteur import MoteurDifferentiel
from robot.controleur import ControleurClavierPygame
from robot.vue import VuePygame


robot = RobotMobile(moteur=MoteurDifferentiel())
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
    robot.mettre_a_jour(dt)

    vue.dessiner_robot(robot)
    vue.tick(60)

pygame.quit()
