from robot.robot_mobile import RobotMobile
from robot.moteur import MoteurDifferentiel
from robot.controleur import ControleurTerminal
from robot.vue import VueTerminal


robot = RobotMobile(moteur=MoteurDifferentiel())
controleur = ControleurTerminal()
vue = VueTerminal()

dt = 1.0
running = True

while running:

    vue.dessiner_robot(robot)

    commande = controleur.lire_commande()

    robot.commander(**commande)
    robot.mettre_a_jour(dt)
