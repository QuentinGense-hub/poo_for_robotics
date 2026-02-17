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
        if self.collision() or self.collision_bord():
            # Annulation déplacement
            self.robot.set_position(ancien_x, ancien_y)

    def collision(self):

        for obstacle in self.obstacles:
            if obstacle.collision(self.robot):
                return True

        return False

    def collision_bord(self):

        x = self.robot.x
        y = self.robot.y
        r = self.robot.rayon

        # Limites monde centré en (0,0)
        demi_largeur = self.largeur / 2
        demi_hauteur = self.hauteur / 2

        if x - r < -demi_largeur:
            return True
        if x + r > demi_largeur:
            return True
        if y - r < -demi_hauteur:
            return True
        if y + r > demi_hauteur:
            return True

        return False