from robot.mur import Mur

def creer_carte(env, grille, taille_case=0.5):
    """
    grille: liste de strings. # => mur, . => dot/point, espace => rien
    coordonnée: i=col, j=row
    on positionne (0,0) en haut-left si tu veux, mais ici on place en coordonnées (x,y)
    """
    hauteur = len(grille)
    largeur = len(grille[0])
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
            # autres symboles possibles à ajouter...