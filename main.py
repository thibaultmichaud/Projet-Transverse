import pygame


pygame.init()

LARGEUR, HAUTEUR = 800, 600
GRAVITE = 0.5
VITESSE_JOUEUR = 5
SAUT_FORCE = -15

ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Jeu de Plateforme")

BLANC = (255, 255, 255)

fond_image = pygame.image.load("Fond.jpg")
fond_image = pygame.transform.scale(fond_image, (LARGEUR, HAUTEUR))

joueur_image_original = pygame.image.load("Goku2.png")
joueur_image_original = pygame.transform.scale(joueur_image_original, (40, 60))


class Joueur:
    def __init__(self):
        self.rect = pygame.Rect(100, HAUTEUR - 100, 45, 150)
        self.vitesse_y = 0
        self.au_sol = False
        self.direction = 1  # 1 = droite, -1 = gauche
        self.joueur_image = joueur_image_original  # Image par défaut non inversée

    def deplacer(self, touches):
        if touches[pygame.K_LEFT]:
            self.rect.x -= VITESSE_JOUEUR
            self.direction = -1
        if touches[pygame.K_RIGHT]:
            self.rect.x += VITESSE_JOUEUR
            self.direction = 1

        if touches[pygame.K_SPACE] and self.au_sol:
            self.sauter()

        self.mettre_a_jour_image()

    def sauter(self):
        self.vitesse_y = SAUT_FORCE
        self.au_sol = False

    def appliquer_gravite(self):
        self.vitesse_y += GRAVITE
        self.rect.y += self.vitesse_y

        if self.rect.y >= HAUTEUR - self.rect.height:
            self.rect.y = HAUTEUR - self.rect.height
            self.vitesse_y = 0
            self.au_sol = True

    def mettre_a_jour_image(self):
        if self.direction == -1:
            self.joueur_image = pygame.transform.flip(joueur_image_original, True, False)
        else:
            self.joueur_image = joueur_image_original

    def dessiner(self, surface):
        surface.blit(self.joueur_image, (self.rect.x, self.rect.y))


def jeu():
    clock = pygame.time.Clock()
    joueur = Joueur()

    en_cours = True
    while en_cours:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False

        touches = pygame.key.get_pressed()
        joueur.deplacer(touches)
        joueur.appliquer_gravite()

        ecran.blit(fond_image, (0, 0))  # Afficher l'image de fond
        joueur.dessiner(ecran)
        pygame.display.flip()

    pygame.quit()

jeu()

