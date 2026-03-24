import pygame
from robot.pacman import Pacman
from robot.ghost import Ghost
from robot.moteur import MoteurDifferentiel
from robot.vue import VuePygame
from robot.environnement import Environnement
from robot.map_loader import creer_carte

if __name__ == "__main__":
    taille_case = 1.0

    # Exemple de grille simple : # murs ; . points ; space libre
    grille = [
        "############################",
        "#............##............#",
        "#.#........#.##.#........#.#",
        "#.#........#.##.#........#.#",
        "#.####..####.##.####..####.#",
        "#............P.............#",
        "#......##..######..##......#",
        "#......##....##....##......#",
        "####...##... ## ...##...####",
        "   #...#    GGGG    #...#   ",
        "####...#  ########  #...####",
        "#............##............#",
        "#............##............#",
        "#...##................##...#",
        "###.##.##.########.##.##.###",
        "#......##....##....##......#",
        "#......##....##....##......#",
        "#..........................#",
        "############################"
    ]

    env = Environnement(
        largeur=len(grille[0]) * taille_case,
        hauteur=len(grille) * taille_case
    )
    creer_carte(env, grille, taille_case=taille_case)

    # créer pacman
    px, py = env.pacman_spawn
    pac = Pacman(x=px, y=py,
                 moteur=MoteurDifferentiel(v=0.0, omega=0.0, vmax=1.5, omegamax=4.0),
                 rayon=0.25)
    env.ajouter_robot(pac)

    # créer un fantôme
    env.spawn_ghosts()

    scale = 40

    largeur_px = int(env.largeur * scale)
    hauteur_px = int(env.hauteur * scale)

    vue = VuePygame(largeur_px, hauteur_px)
    vue.scale = scale
    
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