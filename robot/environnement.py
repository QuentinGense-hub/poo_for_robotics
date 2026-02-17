class Environnement:

    def __init__(self, largeur=10, hauteur=10):
        self.largeur = largeur
        self.hauteur = hauteur
        self.robot = None
        self.obstacles = []

    def ajouter_robot(self, robot):
        self.robot = robot

    def ajouter_obstacle(self, obstacle):
        self.obstacles.append(obstacle)

    def mettre_a_jour(self, dt):

        # Sauvegarde ancienne position
        ancien_x = self.robot.x
        ancien_y = self.robot.y

        # Le robot calcule son mouvement
        self.robot.mettre_a_jour(dt)

        # Vérification collision
        if self.collision():
            # Annulation déplacement
            self.robot.set_position(ancien_x, ancien_y)

    def collision(self):

        for obstacle in self.obstacles:
            if obstacle.collision(self.robot):
                return True

        return False