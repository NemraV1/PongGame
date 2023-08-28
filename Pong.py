import pygame
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
screen_width = 800
screen_height = 600

# Création de l'écran
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong Game")

# Charger l'image de fond (remplacez "background.jpg" par le chemin de votre image)
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Polices de texte
font = pygame.font.Font(None, 48)

# Couleurs
white = (255, 255, 255)
black = (0, 0, 0)

# Raquettes et balle
player1 = pygame.Rect(screen_width - 20, screen_height // 2 - 40, 10, 80)
player2 = pygame.Rect(10, screen_height // 2 - 40, 10, 80)
ball = pygame.Rect(screen_width // 2 - 15, screen_height // 2 - 15, 30, 30)

# Vitesse de déplacement
player_speed = 6  # Légèrement augmenté
ball_speed = 5
ball_speed_x = ball_speed * random.choice((1, -1))
ball_speed_y = ball_speed * random.choice((1, -1))

# Scores
player1_score = 0
player2_score = 0
max_score = 10

# Effet d'impact
impact_sound = pygame.mixer.Sound("impact.wav")

# Compteur de rebonds sur la raquette du joueur 1
player1_bounce_count = 0
bounce_threshold = 5  # Nombre de rebonds nécessaires pour augmenter la vitesse

# Menu
menu_active = False

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player1.y -= player_speed
    if keys[pygame.K_DOWN]:
        player1.y += player_speed
    if keys[pygame.K_w]:
        player2.y -= player_speed
    if keys[pygame.K_s]:
        player2.y += player_speed
    if keys[pygame.K_RETURN] and menu_active:
        menu_active = False
        player1_score = 0
        player2_score = 0
        ball = pygame.Rect(screen_width // 2 - 15, screen_height // 2 - 15, 30, 30)
        ball_speed_x = ball_speed * random.choice((1, -1))
        ball_speed_y = ball_speed * random.choice((1, -1))
        player1_bounce_count = 0  # Réinitialiser le compteur de rebonds

    # Déplacement des raquettes
    player1.y = max(player1.y, 0)
    player1.y = min(player1.y, screen_height - player1.height)
    player2.y = max(player2.y, 0)
    player2.y = min(player2.y, screen_height - player2.height)

    # Déplacement de la balle
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Rebond de la balle sur les bords
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y = -ball_speed_y

    # Rebond de la balle sur les raquettes
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed_x = -ball_speed_x
        impact_sound.play()

        # Augmenter le compteur de rebonds du joueur 1
        if ball_speed_x > 0:  # Assurez-vous que la balle va vers le joueur 1
            player1_bounce_count += 1
            if player1_bounce_count >= bounce_threshold:
                ball_speed_x *= 1.05  # Augmenter légèrement la vitesse

    # Gestion du score
    if ball.left <= 0:
        player1_score += 1
        if player1_score == max_score:
            menu_active = True
        else:
            ball = pygame.Rect(screen_width // 2 - 15, screen_height // 2 - 15, 30, 30)
            ball_speed_x = ball_speed * random.choice((1, -1))
            ball_speed_y = ball_speed * random.choice((1, -1))
            player1_bounce_count = 0  # Réinitialiser le compteur de rebonds

    if ball.right >= screen_width:
        player2_score += 1
        if player2_score == max_score:
            menu_active = True
        else:
            ball = pygame.Rect(screen_width // 2 - 15, screen_height // 2 - 15, 30, 30)
            ball_speed_x = ball_speed * random.choice((1, -1))
            ball_speed_y = ball_speed * random.choice((1, -1))

    # Affichage
    screen.blit(background_image, (0, 0))  # Afficher l'image de fond
    pygame.draw.rect(screen, white, player1)
    pygame.draw.rect(screen, white, player2)
    pygame.draw.ellipse(screen, white, ball)
    player1_score_text = font.render(str(player1_score), True, white)
    player2_score_text = font.render(str(player2_score), True, white)
    screen.blit(player1_score_text, (screen_width - 60, 20))
    screen.blit(player2_score_text, (40, 20))

    # Affichage du menu
    if menu_active:
        menu_text = font.render("Game Over", True, white)
        menu_text_rect = menu_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(menu_text, menu_text_rect)
        restart_text = font.render("Appuyez sur Entrée pour rejouer", True, white)
        restart_text_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 60))
        screen.blit(restart_text, restart_text_rect)

    pygame.display.flip()

    # Limiter les FPS
    pygame.time.Clock().tick(60)

# Quitter Pygame
pygame.quit()
