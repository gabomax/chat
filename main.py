import pygame
import time
pygame.init()

# Définir les constantes pour l'écran
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

# Définir les couleurs
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Définir la classe joueur
class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height, initial_position):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.speed = 5

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        
        # Vérifier si le joueur est sorti de l'écran et le faire réapparaître de l'autre côté
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        elif self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
            
# Définir la classe obstacle
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, color, width, height, position):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = position

# Initialiser les scores
chat_score = 0
mouse_score = 0

# Définir le temps de départ
start_time = time.time()

# Initialiser la fenêtre de jeu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chat et Souris Multi-joueurs")

# Initialiser les joueurs
player1 = Player(RED, 50, 50, (100, 100)) # Chat
player2 = Player(BLUE, 50, 50, (900, 400)) # Souris

# Créer un groupe pour les joueurs
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)

# Ajouter des obstacles
obstacle1 = Obstacle(WHITE, 100, 20, (300, 200))
obstacle2 = Obstacle(WHITE, 20, 100, (500, 300))
obstacle3 = Obstacle(WHITE, 20, 300, (200, 300))
obstacle4 = Obstacle(WHITE, 20, 180, (500, 50))
obstacle5 = Obstacle(WHITE, 300, 20, (300, 500))
obstacle6 = Obstacle(WHITE, 280, 20, (800, 200))
obstacle7 = Obstacle(WHITE, 20, 280, (800, 250))
obstacle8 = Obstacle(WHITE, 100, 20, (0, 300))
obstacles.add(obstacle1)
obstacles.add(obstacle2)
obstacles.add(obstacle3)
obstacles.add(obstacle4)
obstacles.add(obstacle5)
obstacles.add(obstacle6)
obstacles.add(obstacle7)
obstacles.add(obstacle8)
all_sprites.add(obstacles)

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Logique du jeu (déplacement des joueurs, etc.)
    keys = pygame.key.get_pressed()
    player1_dx, player1_dy = 0, 0
    player2_dx, player2_dy = 0, 0

    if keys[pygame.K_z]:
        player1_dy = -1
    if keys[pygame.K_s]:
        player1_dy = 1
    if keys[pygame.K_q]:
        player1_dx = -1
    if keys[pygame.K_d]:
        player1_dx = 1

    if keys[pygame.K_UP]:
        player2_dy = -1
    if keys[pygame.K_DOWN]:
        player2_dy = 1
    if keys[pygame.K_LEFT]:
        player2_dx = -1
    if keys[pygame.K_RIGHT]:
        player2_dx = 1

    player1.move(player1_dx, player1_dy)
    player2.move(player2_dx, player2_dy)
    
    
    if pygame.sprite.collide_rect(player1, player2):
        # La souris est attrapée par le chat
        chat_score += 1
        
        player1.rect.topleft = (100, 100)
        player2.rect.topleft = (900, 400)
        start_time = time.time()

    
    if time.time() - start_time >= 60:
        # La souris a survécu 60 secondes
        mouse_score += 1
        
        player1.rect.topleft = (100, 100)
        player2.rect.topleft = (900, 400)
        
        start_time = time.time()
        
    # Vérifier la collision entre les joueurs et les obstacles
    for obstacle in pygame.sprite.spritecollide(player1, obstacles, False):
        player1.rect.x -= player1_dx * player1.speed
        player1.rect.y -= player1_dy * player1.speed

    for obstacle in pygame.sprite.spritecollide(player2, obstacles, False):
        player2.rect.x -= player2_dx * player2.speed
        player2.rect.y -= player2_dy * player2.speed


    # Effacer l'écran
    screen.fill(BLACK)

    # Dessiner les joueurs
    all_sprites.draw(screen)
    
    # Afficher les scores
    font = pygame.font.Font(None, 36)
    chat_text = font.render(f"Score du chat: {chat_score}", True, RED)
    mouse_text = font.render(f"Score de la souris: {mouse_score}", True, BLUE)
    screen.blit(chat_text, (10, 10))
    screen.blit(mouse_text, (10, 40))    
    
    # Afficher le chronomètre
    elapsed_time = time.time() - start_time
    timer_text = font.render(f"Temps écoulé: {int(elapsed_time)} secondes", True, WHITE)
    screen.blit(timer_text, (10, 70))

    # Mettre à jour l'écran
    pygame.display.flip()

    # Limiter le nombre d'images par seconde
    pygame.time.Clock().tick(60)

pygame.quit()