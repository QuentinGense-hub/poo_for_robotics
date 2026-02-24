import math
import pygame

class EntiteMobile:
    def __init__(self, x, y, vitesse=2.0, rayon=12):
        self.x = float(x)
        self.y = float(y)

        self.vitesse = vitesse
        self.rayon = rayon

        # Direction en radians
        self.angle = 0.0

        # Vitesse angulaire (pour tourner en arc)
        self.vitesse_rotation = 0.08

        # Vecteur vitesse
        self.vx = 0.0
        self.vy = 0.0

        self.actif = True

    # Mise à jour
    def update(self, obstacles):
        self.calcul_vecteur_vitesse()
        self.deplacer(obstacles)

    # Calcul du vecteur
    def calcul_vecteur_vitesse(self):
        self.vx = self.vitesse * math.cos(self.angle)
        self.vy = self.vitesse * math.sin(self.angle)

    # Déplacement continu
    def deplacer(self, obstacles):
        prochain_x = self.x + self.vx
        prochain_y = self.y + self.vy

        if not self.collision(prochain_x, prochain_y, obstacles):
            self.x = prochain_x
            self.y = prochain_y

    # Rotation
    def tourner_gauche(self):
        self.angle -= self.vitesse_rotation

    def tourner_droite(self):
        self.angle += self.vitesse_rotation

    # Collision cercle / rectangle
    def collision(self, x, y, obstacles):
        for obstacle in obstacles:
            if self.collision_cercle_rectangle(x, y, obstacle):
                return True
        return False

    def collision_cercle_rectangle(self, cx, cy, rect):
        # rect doit être un pygame.Rect
        closest_x = max(rect.left, min(cx, rect.right))
        closest_y = max(rect.top, min(cy, rect.bottom))

        distance_x = cx - closest_x
        distance_y = cy - closest_y

        distance_carre = (distance_x ** 2) + (distance_y ** 2)
        return distance_carre < (self.rayon ** 2)

    # Affichage debug
    def draw(self, screen, couleur=(255, 255, 0)):
        pygame.draw.circle(
            screen,
            couleur,
            (int(self.x), int(self.y)),
            self.rayon
        )
