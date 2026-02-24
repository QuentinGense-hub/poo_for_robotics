import pygame
from robot.robot_mobile import RobotMobile
from robot.moteur import MoteurDifferentiel
from robot.controleur import ControleurClavierPygame
from robot.vue import VuePygame
from robot.environnement import Environnement
from robot.obstacle import ObstacleCirculaire, ObstacleRectangulaire
from robot.mur import Mur
from robot.map_loader import creer_carte

taille_case = 0.5

robot = RobotMobile(
    x=1 * taille_case + taille_case / 2,
    y=1 * taille_case + taille_case / 2,
    moteur=MoteurDifferentiel())
env = Environnement(largeur=10, hauteur=8)

env.ajouter_robot(robot)

PACMAN_MAP = [
"#################",
"#...............#",
"#..###.###.###...#",
"#..............#",
"#..###.#.#.###...#",
"#......#.#......#",
"######.#.#.######",
"#...............#",
"#...###.###.###...#",
"#...............#",
"#...............#",
"#################"
]

creer_carte(env, PACMAN_MAP, taille_case=0.5)

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
