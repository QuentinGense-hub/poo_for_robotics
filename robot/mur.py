from robot.obstacle import ObstacleRectangulaire


class Mur(ObstacleRectangulaire):
    """
Mur = simple obstacle rectangulaire utilisé pour construire une carte
"""

    def __init__(self, x, y, largeur, hauteur):
        super().__init__(x, y, largeur, hauteur)