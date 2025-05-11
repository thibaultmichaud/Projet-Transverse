# Importation des bibliothèques nécessaires
import pygame
import random

# Initialisation de Pygame
pygame.init()

# Chargement et lecture en boucle de la musique d’ambiance
pygame.mixer.music.load("musique-d'ambiance.mp3")
pygame.mixer.music.set_volume(0.2)  # Volume de la musique
pygame.mixer.music.play(-1)  # Lecture en boucle infinie

# Dimensions du joueur
taille_joueur = 50

# Création de la fenêtre du jeu
largeur_ecran = 800
hauteur_ecran = 600
ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
pygame.display.set_caption("Jump or Death ")

# Chargement et mise à l’échelle du fond d’écran
fond_original = pygame.image.load("fdc2.png")
fond = pygame.transform.scale(fond_original, (largeur_ecran, hauteur_ecran))
position_fond_x = 0  # Position horizontale du fond (pour le défilement)

# Image affichée en cas de Game Over
image_gameover = pygame.image.load("Gameovermenu.png")
image_gameover = pygame.transform.scale(image_gameover, (largeur_ecran, hauteur_ecran))

# Chargement des sprites
image_sol = pygame.image.load("sol2.png").convert_alpha()
image_sol = pygame.transform.scale(image_sol, (100, 50))
image_plateforme = pygame.image.load("Plateforme.png").convert_alpha()
image_monstre = pygame.image.load("New Piskel-1.png (1).png").convert_alpha()
image_joueur = pygame.image.load("Perso_principal.png").convert_alpha()
image_joueur = pygame.transform.scale(image_joueur, (taille_joueur, taille_joueur))

# Définition de quelques couleurs utiles
blanc = (255, 255, 255)
noir = (0, 0, 0)
vert = (0, 255, 0)
rouge = (255, 0, 0)
gris = (200, 200, 200)
bleu = (100, 100, 255)

# Contrôle du nombre de FPS
clock = pygame.time.Clock()

# Position et vitesse initiale du joueur
joueur_x = largeur_ecran / 2 - taille_joueur / 2
joueur_y = hauteur_ecran - taille_joueur
vitesse_joueur_x = 0
vitesse_joueur_y = 0
gravite = 1
saut = -20  # Force du saut
sur_sol = False  # Pour vérifier si le joueur touche le sol
double_saut_dispo = False  # Autorisation du double saut
particules = []  # Liste des particules pour les effets visuels

# Variables du terrain
hauteur_sol = 50
sol_y = hauteur_ecran - hauteur_sol
largeur_segment_sol = 100
tableau_sol = []  # Segments du sol
monstres = []  # Monstres au sol
plateformes = []  # Plateformes flottantes
monstres_aeriens = []  # Monstres qui volent

# États possibles du jeu : menu, jeu en cours, gameover
etat_jeu = "menu"
score = 0
niveau = 1

# Chargement des sons
son_saut = pygame.mixer.Sound("saut_classique.wav")
son_gameover = pygame.mixer.Sound("gameover2.wav")
son_saut.set_volume(0.1)
son_gameover.set_volume(3)

#  Fonctions utiles

# Affiche du texte centré à l’écran
def afficher_texte(texte, taille, couleur, x, y, gras=False):
    font = pygame.font.Font("dogicapixel.ttf", 15)
    if gras:
        font.set_bold(True)
    surface_texte = font.render(texte, True, couleur)
    rect_texte = surface_texte.get_rect(center=(x, y))
    ecran.blit(surface_texte, rect_texte)

# Dessine une boîte semi-transparente pour le menu ou les scores
def dessiner_boite_transparente(x, y, largeur, hauteur, couleur=(30, 30, 30), opacite=200):
    boite = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
    boite.fill((*couleur, opacite))
    pygame.draw.rect(boite, (255, 255, 255, 40), boite.get_rect(), width=2, border_radius=15)
    ecran.blit(boite, (x, y))

# Affiche un bouton cliquable avec du texte
def dessiner_bouton_texte(texte, x, y, largeur, hauteur):
    bouton = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
    bouton.fill((60, 60, 60, 220))
    pygame.draw.rect(bouton, (255, 255, 255, 80), (0, 0, largeur, hauteur), 2, border_radius=10)
    ecran.blit(bouton, (x, y))
    afficher_texte(texte, 28, blanc, x + largeur // 2, y + hauteur // 2)
    return pygame.Rect(x, y, largeur, hauteur)

# Génère le sol, les monstres et les plateformes au début du jeu
def generer_sol_initial():
    global tableau_sol, joueur_x, monstres, plateformes, monstres_aeriens, sol_y
    tableau_sol = []
    monstres = []
    plateformes = []
    monstres_aeriens = []
    for i in range(largeur_ecran // largeur_segment_sol + 5):
        hauteur_variable = random.randint(0, 40 + min(score, 100))
        sol_y = hauteur_ecran - hauteur_sol - hauteur_variable
        is_terre = i < 5 or random.random() < 0.75  # Plus de terre au début
        tableau_sol.append((i * largeur_segment_sol, is_terre, sol_y))
        # Ajoute un monstre au sol
        if is_terre and i >= 5 and random.random() < 0.2:
            monstres.append(pygame.Rect(i * largeur_segment_sol + largeur_segment_sol // 2, sol_y - 30, 30, 30))
        # Ajoute une plateforme flottante (et parfois un monstre volant)
        if random.random() < 0.15:
            p_y = sol_y - random.randint(100, 250)
            plateformes.append(pygame.Rect(i * largeur_segment_sol, p_y, 80, 20))
            if random.random() < 0.3:
                monstres_aeriens.append({
                    "rect": pygame.Rect(i * largeur_segment_sol + 20, p_y - 30, 30, 30),
                    "dir": random.choice([-1, 1])
                })
    joueur_x = tableau_sol[2][0]  # Position initiale du joueur

# Ajoute un effet de particules (petits cercles gris) lors du saut
def ajouter_particules(x, y):
    for _ in range(8):
        particules.append([[x, y], [random.uniform(-1, 1), random.uniform(-3, 0)], random.randint(10, 20)])

# Met à jour et dessine les particules à l’écran
def mettre_a_jour_particules():
    for p in particules:
        p[0][0] += p[1][0]
        p[0][1] += p[1][1]
        p[2] -= 1
    particules[:] = [p for p in particules if p[2] > 0]
    for p in particules:
        pygame.draw.circle(ecran, gris, (int(p[0][0]), int(p[0][1])), 3)

# Met à jour la position du sol, des monstres, plateformes et du fond pour créer l’effet de déplacement
def generer_sol():
    global score, position_fond_x, sol_y

    # Fait défiler les segments du sol vers la gauche
    for i in range(len(tableau_sol)):
        tableau_sol[i] = (tableau_sol[i][0] - vitesse_joueur_x, tableau_sol[i][1], tableau_sol[i][2])

    # Déplace les monstres au sol
    for m in monstres:
        m.x -= vitesse_joueur_x

    # Déplace et anime les monstres volants
    for m in monstres_aeriens:
        m["rect"].x -= vitesse_joueur_x
        m["rect"].x += m["dir"]  # Déplacement latéral
        if random.random() < 0.01:  # Changement aléatoire de direction
            m["dir"] *= -1

    # Déplace les plateformes flottantes
    for p in plateformes:
        p.x -= vitesse_joueur_x

    # Défilement infini du fond d’écran
    position_fond_x -= vitesse_joueur_x // 2
    if position_fond_x <= -largeur_ecran:
        position_fond_x = 0
    elif position_fond_x >= largeur_ecran:
        position_fond_x = -largeur_ecran

    # Génération d’un nouveau segment à droite quand un sort de l’écran à gauche
    if tableau_sol[0][0] < -largeur_segment_sol:
        tableau_sol.pop(0)
        hauteur_variable = random.randint(0, 40 + min(score, 100))
        sol_y = hauteur_ecran - hauteur_sol - hauteur_variable
        is_terre = random.random() < 0.75
        tableau_sol.append((tableau_sol[-1][0] + largeur_segment_sol, is_terre, sol_y))

        # Ajoute parfois un nouveau monstre ou une plateforme
        if is_terre and random.random() < 0.2:
            monstres.append(pygame.Rect(tableau_sol[-1][0] + largeur_segment_sol // 2, sol_y - 30, 30, 30))
        if random.random() < 0.15:
            p_y = sol_y - random.randint(100, 250)
            p_rect = pygame.Rect(tableau_sol[-1][0], p_y, 80, 20)
            plateformes.append(p_rect)
            if random.random() < 0.3:
                monstres_aeriens.append({"rect": pygame.Rect(p_rect.x + 20, p_y - 30, 30, 30), "dir": random.choice([-1, 1])})

        # Incrémentation du score à chaque nouveau segment
        score += 1

    # Affichage des éléments à l’écran
    for x, sol, y in tableau_sol:
        if sol:
            ecran.blit(image_sol, (x, y))
    for m in monstres:
        ecran.blit(pygame.transform.scale(image_monstre, (m.width, m.height)), m.topleft)
    for m in monstres_aeriens:
        ecran.blit(pygame.transform.scale(image_monstre, (m["rect"].width, m["rect"].height)), m["rect"].topleft)
    for p in plateformes:
        ecran.blit(pygame.transform.scale(image_plateforme, (p.width, p.height)), p.topleft)
# Génération initiale du terrain au lancement
generer_sol_initial()

# Boucle principale infinie du jeu
while True:
    # Gestion des événements (clavier, souris, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # Clic sur "Quitter" dans les menus
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if etat_jeu in ["menu", "gameover"] and bouton_quitter.collidepoint(pos):
                pygame.quit()
                quit()

        # Depuis le menu : appuyer sur espace pour commencer
        if etat_jeu == "menu" and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            etat_jeu = "jeu"
            generer_sol_initial()
            joueur_y = hauteur_ecran - taille_joueur
            vitesse_joueur_x = 0
            vitesse_joueur_y = 0
            score = 0
            particules.clear()
            double_saut_dispo = False

        # Depuis le gameover : appuyer sur espace pour retourner au menu
        elif etat_jeu == "gameover" and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            etat_jeu = "menu"

        # Contrôles du personnage pendant la partie
        elif etat_jeu == "jeu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    vitesse_joueur_x = -8
                elif event.key == pygame.K_RIGHT:
                    vitesse_joueur_x = 8
                elif event.key == pygame.K_SPACE:
                    if sur_sol or double_saut_dispo:
                        vitesse_joueur_y = saut
                        son_saut.play()
                        ajouter_particules(joueur_x + taille_joueur // 2, joueur_y + taille_joueur)
                        if not sur_sol:
                            double_saut_dispo = False
                        sur_sol = False
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    vitesse_joueur_x = 0

    # Efface l’écran à chaque frame
    ecran.fill(noir)

    #  État MENU
    if etat_jeu == "menu":
        # Affiche deux fonds qui défilent pour l’animation
        ecran.blit(fond, (0, 0))
        ecran.blit(fond, (largeur_ecran, 0))

        # Boîte transparente au centre du menu
        dessiner_boite_transparente(200, 150, 400, 300)

        # Titre du jeu
        afficher_texte("Jump or Death", 64, blanc, largeur_ecran / 2, 190, gras=True)

        # Texte qui clignote (toutes les 1000 ms)
        clignotement = (pygame.time.get_ticks() % 1000) < 600
        if clignotement:
            afficher_texte("Appuyez sur ESPACE pour jouer", 28, blanc, largeur_ecran / 2, 290)

        # Bouton pour quitter
        bouton_quitter = dessiner_bouton_texte("Quitter le jeu", largeur_ecran // 2 - 100, 360, 200, 50)

    # === État EN JEU ===
    elif etat_jeu == "jeu":
        # Affichage du fond qui défile
        ecran.blit(fond, (position_fond_x, 0))
        ecran.blit(fond, (position_fond_x + largeur_ecran, 0))

        # Mise à jour de la position verticale du joueur avec la gravité
        joueur_y += vitesse_joueur_y
        vitesse_joueur_y += gravite

        # Création du rectangle de collision du joueur
        joueur_rect = pygame.Rect(joueur_x, joueur_y, taille_joueur, taille_joueur)
        sur_sol = False  # On vérifie à chaque frame si le joueur est sur une surface

        # === COLLISIONS AVEC LE SOL ===
        for x, sol, y in tableau_sol:
            if sol and joueur_x + taille_joueur > x and joueur_x < x + largeur_segment_sol and joueur_y + taille_joueur >= y:
                joueur_y = y - taille_joueur
                vitesse_joueur_y = 0
                sur_sol = True
                double_saut_dispo = True
                break

        # === COLLISIONS AVEC LES PLATEFORMES ===
        for p in plateformes:
            if joueur_rect.colliderect(p) and vitesse_joueur_y >= 0:
                joueur_y = p.top - taille_joueur
                vitesse_joueur_y = 0
                sur_sol = True
                double_saut_dispo = True

        # === COLLISIONS AVEC LES MONSTRES ===
        for m in monstres:
            if joueur_rect.colliderect(m):
                son_gameover.play()
                etat_jeu = "gameover"
        for m in monstres_aeriens:
            if joueur_rect.colliderect(m["rect"]):
                son_gameover.play()
                etat_jeu = "gameover"

        # Si le joueur tombe hors de l’écran
        if joueur_y > hauteur_ecran:
            son_gameover.play()
            etat_jeu = "gameover"

        # Affiche le sprite du joueur
        ecran.blit(image_joueur, joueur_rect.topleft)

        # Génère et affiche le décor, les monstres et plateformes
        generer_sol()

        # Met à jour et dessine les particules
        mettre_a_jour_particules()

        # Affiche le score en haut à gauche
        afficher_texte(f"Score: {score}", 30, blanc, 100, 50)

    #  État GAME OVER
    elif etat_jeu == "gameover":
        # Affiche l’image de Game Over
        ecran.blit(image_gameover, (0, 0))

        # Menu avec le score
        dessiner_boite_transparente(200, 150, 400, 300)
        afficher_texte("GAME OVER", 64, rouge, largeur_ecran / 2, 190, gras=True)
        afficher_texte(f"Score : {score}", 28, blanc, largeur_ecran / 2, 260)

        # Message qui clignote pour rejouer
        clignotement = (pygame.time.get_ticks() % 1000) < 600
        if clignotement:
            afficher_texte("Appuyez sur ESPACE pour recommencer", 26, blanc, largeur_ecran / 2, 310)

        # Bouton pour quitter
        bouton_quitter = dessiner_bouton_texte("Quitter le jeu", largeur_ecran // 2 - 100, 370, 200, 50)

    # Rafraîchissement de l’écran
    pygame.display.flip()
    # Limite les images à 60 par seconde
    clock.tick(60)
