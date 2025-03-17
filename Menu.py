import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

font = pygame.font.Font(None, 74)
text_play = font.render("Jouer", True, (255, 255, 255))
text_options = font.render("Options", True, (255, 255, 255))
text_quit = font.render("Quitter", True, (255, 255, 255))

play_rect = pygame.Rect(300, 200, 200, 100)
options_rect = pygame.Rect(300, 350, 200, 100)
quit_rect = pygame.Rect(300, 500, 200, 100)

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(text_play, (play_rect.x + 50, play_rect.y + 25))
    screen.blit(text_options, (options_rect.x + 35, options_rect.y + 25))
    screen.blit(text_quit, (quit_rect.x + 50, quit_rect.y + 25))

    pygame.draw.rect(screen, (0, 128, 255), play_rect, 2)
    pygame.draw.rect(screen, (0, 128, 255), options_rect, 2)
    pygame.draw.rect(screen, (0, 128, 255), quit_rect, 2)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):
                print("Jouer")
            elif options_rect.collidepoint(event.pos):
                print("Options")
            elif quit_rect.collidepoint(event.pos):
                print("Quitter")