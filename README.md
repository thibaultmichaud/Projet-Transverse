# Projet-Transverse

Jump or Death - Carnet de bord du projet

Présentation du projet : 

Jump or Death est un jeu de plateforme développé en Python à l'aide de la bibliothèque Pygame, dans le cadre du projet transverse. Le but du jeu est de contrôler un personnage capable de se déplacer, sauter et éviter des ennemis sur des plateformes. Le joueur doit survivre le plus longtemps possible. Chaque case passée équivaut à 1 point marqué.

Étapes du développement : 

Conception : 
Réflexion sur les mécaniques de jeu : type runner en scrolling horizontal.
Définition de l’univers graphique : ambiance pixel, animations simples.
Création d’une arborescence de projet propre et organisée.
Répartition des rôles entre les membres de l’équipe.

Moteur de jeu : 
Mise en place de la fenêtre de jeu avec Pygame.
Création du personnage principal avec Piskel (site pour créer des personnages en pixel)
les mouvements du personnage :
Marche à gauche et à droite avec animations.
Saut avec animation (grâce aux trajectoires)
Gestion des collisions avec le sol et les plateformes, lorsque le personnage saute, des particules ont été ajoutées pour plus d’immersion.

Décor et environnement : 
Intégration de plateformes fixes et d’ennemis générés aléatoirement.
Utilisation de plusieurs fichiers d’image pour le décor en compilant les éléments ensemble (cubes de terre + décor de ciel).

Ennemis et collisions : 
Ajout d’ennemis avec un comportement de déplacement ou pas (il y a aussi des ennemis statiques).
Détection de collisions entre le personnage et les ennemis.
Implémentation de la condition de Game Over.

Sons et ambiance : 
Intégration d’une musique de fond.
Effets sonores pour les actions importantes : saut, mort, menu de fin.
Tous les sons ont été placés dans l'arborescence.

Interface et menus : 
Écran de démarrage avec possibilité de lancer ou quitter le jeu.
Affichage du score en temps réel en haut à gauche.
Écran de fin avec menu Game Over et redémarrage possible.
Intégration de polices personnalisées pour améliorer l’aspect visuel.

Notice d’utilisation : 

Lancement : 

Assurez-vous d’avoir installé Python 3 ainsi que la bibliothèque Pygame :
pip install pygame

Ensuite, exécutez le fichier main.py :
python main.py

Commandes : 

Flèche droite : aller à droite
Flèche gauche : aller à gauche
Barre espace : sauter (double saut possible)

Objectif du jeu : 

Survivre le plus longtemps possible en évitant les obstacles et les ennemis, et accumuler un score élevé, durée de temps de jeu sans limite.

Ce qui fonctionne : 

Mouvement fluide du personnage
Détection de collisions
Système de saut fonctionnel
Sons intégrés
Menu de démarrage et de fin
Score en temps réel

Améliorations envisagées : 

Optimisation des ressources
Ajout d’un menu de pause
Meilleure gestion des animations de chute et mort
Ajout de plusieurs niveaux avec décors différents
Système de sauvegarde du meilleur score
Déplacement plus intelligent des ennemis
Version mobile ou jouable en ligne

Organisation du projet :

Arborescence simplifiée :
PythonProjet1/
main.py
Sons (saut, musique, game over)
Images (fond, personnages, plateformes)
Polices personnalisées
Animations : NON, personnage statique mais trajectoires utilisées pour le saut et le déplacement.

Membres du projet : 

Thibault Michaud
Riad Dib
Amine Koumtani
Adam Ben Slama
Eloi Cheng