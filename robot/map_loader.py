from robot.mur import Mur

def creer_carte(env, grille, taille_case=0.5):
    """
    grille: liste de strings. # => mur ; . => point ; G => ghost spawn (cuvette)
    On positionne (0,0) en bas-left (coord y calculée avec len-grille).
    taille_case: taille d'une cellule en unités du monde.
    """
    hauteur = len(grille)
    largeur = len(grille[0]) if hauteur > 0 else 0
    for j, ligne in enumerate(grille):
        for i, cellule in enumerate(ligne):
            x = i * taille_case + taille_case/2
            y = (len(grille) - j - 1) * taille_case + taille_case/2
            if cellule == "#":
                mur = Mur(x, y, taille_case, taille_case)
                env.ajouter_obstacle(mur)
            elif cellule == ".":
                # point a ramasser
                env.ajouter_point(x, y)
            elif cellule == "G":
                # position de spawn de fantôme (cuvette). On n'ajoute pas d'obstacle ici
                # mais on garde la position pour instancier les ghosts plus tard.
                if not hasattr(env, "ghost_spawns"):
                    env.ghost_spawns = []
                env.ghost_spawns.append((x, y))
            elif cellule == "P":
                env.pacman_spawn = (x, y)
            # Possibilité d'ajouter d'autres symboles (o = super pellet, H = sol cuvette, ...)