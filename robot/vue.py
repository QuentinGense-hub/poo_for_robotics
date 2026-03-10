# dans ta classe VuePygame : méthode dessiner_environnement et aides
import pygame
import math

class VuePygame:
    def __init__(self, largeur_px, hauteur_px):
        pygame.init()
        self.screen = pygame.display.set_mode((largeur_px, hauteur_px))
        self.clock = pygame.time.Clock()
        self.scale = 50
        self.w_px = largeur_px
        self.h_px = hauteur_px

    def convertir_coordonnees(self, x, y):
        px = int(x * self.scale)
        py = int(self.h_px - y * self.scale)
        return px, py

    def dessiner_environnement(self, env):
        self.screen.fill((0, 0, 0))  # fond noir type pacman

        # dessiner points
        for (x, y) in env.points:
            px, py = self.convertir_coordonnees(x, y)
            pygame.draw.circle(self.screen, (255, 200, 0), (px, py), max(2, int(0.06 * self.scale)))

        # obstacles (murs)
        for obs in env.obstacles:
            obs.dessiner(self)

        # pacman (robot principal)
        if env.robot:
            px, py = self.convertir_coordonnees(env.robot.x, env.robot.y)
            r_px = max(4, int(env.robot.rayon * self.scale))
            # bouche simple pour indiquer orientation
            theta = env.robot.orientation
            pygame.draw.circle(self.screen, (255, 255, 0), (px, py), r_px)
            # œil
            eye_x = px + int(0.4 * r_px * math.cos(theta))
            eye_y = py - int(0.4 * r_px * math.sin(theta))
            pygame.draw.circle(self.screen, (0,0,0), (eye_x, eye_y), max(1, r_px//4))

            # --- dessiner la "cuvette" / positions de spawn des ghosts si présentes
        if hasattr(env, "ghost_spawns"):
            for (gx, gy) in env.ghost_spawns:
                px, py = self.convertir_coordonnees(gx, gy)
                half = int(0.18 * self.scale)
                rect = pygame.Rect(px-half, py-half, half*2, half*2)
                # fond léger pour la cuvette
                s = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
                s.fill((150, 150, 255, 80))  # bleu clair semi-transparent
                self.screen.blit(s, (rect.x, rect.y))
                # contour
                pygame.draw.rect(self.screen, (100, 100, 200), rect, max(1, int(0.01*self.scale)))

        # ghosts
        for g in env.ghosts:
            px, py = self.convertir_coordonnees(g.x, g.y)
            r_px = max(4, int(g.rayon * self.scale))
            pygame.draw.circle(self.screen, (200, 0, 0), (px, py), r_px)

        pygame.display.flip()

    def tick(self, fps=60):
        self.clock.tick(fps)