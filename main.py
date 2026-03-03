import pygame
from robot.pacman import Pacman
from robot.ghost import Ghost
from robot.moteur import MoteurDifferentiel
from robot.vue import VuePygame
from robot.environnement import Environnement
from robot.map_loader import creer_carte

if __name__ == "__main__":
    taille_case = 0.5

    # Exemple de grille simple : # murs ; . points ; space libre
    grille = [
        "##########",
        "#........#",
        "#.####...#",
        "#........#",
        "##########"
    ]

    env = Environnement(largeur=10*taille_case, hauteur=5*taille_case)
    creer_carte(env, grille, taille_case=taille_case)

    # créer pacman
    pac = Pacman(x=1*taille_case + taille_case/2, y=1*taille_case + taille_case/2,
                 moteur=MoteurDifferentiel(v=0.0, omega=0.0, vmax=1.2, omegamax=4.0),
                 rayon=0.2)
    env.ajouter_robot(pac)

    # créer un fantôme
    ghost = Ghost(x=4*taille_case, y=3*taille_case, rayon=0.2)
    env.ajouter_ghost(ghost)

    vue = VuePygame(800, 600, scale=80.0)
    running = True

    while running:
        dt = vue.clock.tick(60) / 1000.0  # dt en secondes

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # commandes clavier pour Pacman (W/S forward/back, A/D tourner)
        keys = pygame.key.get_pressed()
        v_cmd = 0.0
        omega_cmd = 0.0
        speed = 1.0
        omega_speed = 3.0
        if keys[pygame.K_w]:
            v_cmd += speed
        if keys[pygame.K_s]:
            v_cmd -= speed
        if keys[pygame.K_a]:
            omega_cmd += omega_speed
        if keys[pygame.K_d]:
            omega_cmd -= omega_speed

        pac.commander(v_cmd, omega_cmd)

        env.mettre_a_jour(dt)
        vue.dessiner_environnement(env)

        # petite info console
        pygame.display.set_caption(f"Score: {pac.score}  dots remaining: {len(env.points)}")

    pygame.quit()