from robot.mur import Mur

def creer_carte(env, grille, taille_case=0.5):
    for j, ligne in enumerate(grille):
        for i, cellule in enumerate(ligne):
            if cellule == "#":
                x = i * taille_case + taille_case / 2
                y = j * taille_case + taille_case / 2

                mur = Mur(x, y, taille_case, taille_case)
                env.ajouter_obstacle(mur)