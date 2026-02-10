import math
from robot.robot_mobile import RobotMobile
from robot.moteur import MoteurDifferentiel, MoteurOmnidirectionnel

# moteur différentiel
moteur = MoteurDifferentiel()
robot = RobotMobile(moteur=moteur)

dt = 1.0

robot.afficher()
robot.commander(v=1.0, omega=math.pi / 4)
robot.mettre_a_jour(dt)
robot.afficher()

#moteur omnidirectionnel
moteur2 = MoteurOmnidirectionnel()
robot2 = RobotMobile(moteur=moteur2)

robot2.commander(vx=1.0, vy=1.0, omega=0.0)
robot2.mettre_a_jour(1.0)
robot2.afficher()

print("Nombre total de robots :", RobotMobile.nombre_robots())