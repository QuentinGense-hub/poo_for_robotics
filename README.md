Projet Pacman par Reinforcement Learning

1. Introduction
Ce projet consiste à développer une version modifiée du jeu Pacman en utilisant des concepts de robotique mobile et de Reinforcement Learning (RL).
Contrairement au jeu original, le personnage principal est modélisé comme un robot mobile omnidirectionnel évoluant dans un environnement (ici un labyrinthe fermé) en 2 dimensions. L’objectif est de lui faire apprendre à se déplacer de manière autonome dans ce décore afin de collecter des points le plus rapidement possible et donc optimiser ses déplacements.
L’apprentissage est réalisé à l’aide de l’algorithme PPO (Proximal Policy Optimization).
________________________________________
2. Objectifs du projet
Les objectifs principaux sont :
•	Mettre en œuvre une architecture en programmation orientée objet (POO) ;
•	Simuler un robot mobile dans un environnement fixe ;
•	Concevoir un environnement compatible avec Gymnasium ;
•	Implémenter un système de Reinforcement Learning ;
•	Visualiser le comportement de l’agent.
Ce projet permet de faire le lien entre :
•	robotique,
•	Intelligence Artificielle,
•	RL,
•	et simulation.
________________________________________
3. Technologies utilisées
Python
Langage principal du projet.
Gymnasium
Bibliothèque utilisée pour créer un environnement de Reinforcement Learning personnalisé.
Elle permet de :
•	définir l’espace d’actions,
•	définir l’espace d’observations,
•	gérer les épisodes,
•	calculer les récompenses.
Stable-Baselines3
Bibliothèque utilisée pour entraîner l’agent avec l’algorithme PPO.
Elle permet :
•	d’entraîner le modèle,
•	de sauvegarder la politique apprise,
•	de recharger le modèle pour l’exécution.
PyGame
Utilisé pour afficher la simulation.
Permet de :
•	visualiser le labyrinthe,
•	afficher Pacman et les objets,
•	observer le comportement appris.
NumPy
Utilisé pour les calculs numériques et la manipulation des données.
Matplotlib
Utilisé pour tracer les performances de l’agent pendant l’entraînement.
________________________________________
4. Architecture du projet
Le projet est structuré selon une approche orientée objet.
4.1 Classes principales
•	RobotMobile : classe de base représentant un robot (position, orientation, mouvement)
•	Pacman : robot principal contrôlé par l’agent RL
•	Ghost : ennemi avec une logique de poursuite (ici non utilisée mais potentiellement utilisable pour un projet de double agents)
•	MoteurDifferentiel : modèle de déplacement pour robot différentiel (utilisée pour les tests)
•	MoteurOmnidirectionnel : modèle de déplacement pour Pacman
•	Environnement : contient les objets du monde (murs, points, robots), permet de faire le lien entre les différents objets
•	VuePygame : gère l’affichage graphique
Cette organisation permet de séparer clairement :
•	la logique physique,
•	la logique de contrôle,
•	l’environnement,
•	et l’affichage.
________________________________________
4.2 Structure des fichiers
.
├── main.py
├── train_ppo.py
├── map.txt
├── ppo_pacman.zip
├── robot/
│   ├── pacman_env.py
│   ├── robot_mobile.py
│   ├── moteur.py
│   ├── pacman.py
│   ├── ghost.py
│   ├── environnement.py
│   ├── vue_pygame.py
│   └── map_loader.py
└── logs/
________________________________________
5. Modélisation du robot
Le Pacman est modélisé comme un robot omnidirectionnel.
Il peut recevoir trois commandes :
•	vitesse selon l’axe X
•	vitesse selon l’axe Y
•	vitesse de rotation
Cela permet une liberté de mouvement plus grande qu’un robot classique ou qu’un Pacman original.
Dans notre phase de test, les fantômes étaient modélisés avec un moteur différentiel. Dans nos idées d’avancement de ce projet, nous souhaitions les laisser comme tels afin de donner un avantage au Pacman.
________________________________________
6. Environnement de Reinforcement Learning
L’environnement est défini dans PacmanEnv et suit l’interface Gymnasium.
6.1 Espace d’actions
L’action est continue et composée de :
•	vitesse en X
•	vitesse en Y
•	vitesse angulaire
________________________________________
6.2 Espace d’observations
L’agent reçoit plusieurs informations :
•	distances aux murs (capteurs simulés type lidar)
•	position du robot
•	orientation (cosinus et sinus)
•	direction du pellet le plus proche
•	distance à ce pellet
•	proportion de pellets restants
•	score
Ces observations permettent à l’agent de prendre des décisions adaptées à son environnement.
________________________________________
6.3 Fonction de récompense
La récompense est conçue pour guider l’apprentissage :
•	+1 : PacGomme (les boules que le PacMan doit ramasser) collectée
•	+ bonus : rapprochement d’une PacGomme
•	- pénalité : collision avec un mur
•	- pénalité : immobilité ou stagnation
•	+10 : carte entièrement nettoyée
Cette fonction encourage un comportement efficace et autonome.
________________________________________
7. Algorithme d’apprentissage
Le projet utilise l’algorithme PPO (Proximal Policy Optimization).
Cet algorithme est adapté :
•	aux espaces d’actions continus,
•	aux environnements complexes,
•	à un apprentissage stable.
L’entraînement est réalisé sur plusieurs environnements en parallèle afin d’accélérer le processus.
________________________________________
8. Fonctionnement global
Le cycle d’apprentissage est le suivant :
1.	L’agent observe l’environnement
2.	Il choisit une action
3.	L’environnement évolue
4.	Une récompense est calculée
5.	L’agent met à jour sa politique
Ce processus est répété sur un grand nombre d’itérations.
________________________________________
9. Résultats
Les résultats montrent que :
•	l’agent apprend progressivement à éviter les obstacles
•	il optimise ses déplacements
•	il devient capable de collecter efficacement les PacGommes
Les courbes d’apprentissage montrent une augmentation de la récompense moyenne.
________________________________________
10. Limites du projet
Certaines fonctionnalités restent incomplètes :
•	les fantômes ne sont pas intégrés dans l’entraînement RL ;
•	il n’existe pas de condition de défaite pure et dure, le Pacman n’est donc pas totalement poussé à aller vers la victoire, il peut juste se contenter de rester sur place ou faire des micro-déplacements ;
•	manque d’aide au PAcman pour se sortir d’impasses (comme être bloqué dans un coin à cause d’une mauvaise prise de décision).
Ayant 25h pour faire ce projet sans avoir énormément de bagages en robotique et POO, nous avons pris la décision de nous pencher uniquement sur l’entrainement de la récolte du Pacman. Nous n’avons donc pas totalement « respecté » le concept du Pacman. Il se bloque encore dans des situations où il décide de ne pas avancer/ramasser des Pacgomme, préférant ne pas finir plutôt que de prendre le risque de perdre des points.
Il faut donc voir ce code comme une première partie d’un projet et non une version finale.
________________________________________
11. Améliorations possibles
Plusieurs extensions peuvent être envisagées :
•	intégrer les fantômes dans l’environnement RL et donc faire de la POO à double agents ;
•	ajouter une condition de perte ;
•	évoluer plus vers l’esprit du Pacman original ;
•	améliorer les observations et les poids des récompenses.
________________________________________
12. Conclusion
Ce projet permet d’explorer l’application du Reinforcement Learning à un problème inspiré du jeu Pacman, tout en introduisant des concepts de robotique mobile.
Notre principale préoccupation était de réussir à optimiser le parcours du Pacman, tout en le programmant et le gérant comme un robot (et donc de pouvoir gérer le moteur et le lidar). Grace aux résultats concluants des tests fait avec les versions des robots, nous avons pu rapidement nous tourner vers du RL, permettant une belle avancée sur le domaine. Ce projet nous a permit de nous améliorer sur la robotique et la POO, mais aussi sur le RL.
