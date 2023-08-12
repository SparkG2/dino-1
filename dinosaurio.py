import pygame
import random
import os

# Configuración de la pantalla
pygame.init()
WIDTH, HEIGHT = 800, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Dino Run")

# Directorio donde se encuentra este script
script_dir = os.path.dirname(__file__)

# Cargar imágenes
background_img = pygame.image.load(os.path.join(script_dir, "background.png")).convert()
dino_img = pygame.image.load(os.path.join(script_dir, "dino.png")).convert_alpha()
cactus_img = pygame.image.load(os.path.join(script_dir, "cactus.png")).convert_alpha()

# Escalar imagen de fondo inicial
scaled_background = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Variables del dino
dino_rect = dino_img.get_rect()
dino_rect.topleft = (50, HEIGHT - dino_rect.height)
dino_y_speed = 0
GRAVITY = 1

# Obstáculos
obstacles = []

# Reloj para controlar la velocidad del juego
clock = pygame.time.Clock()

# Variables para el estado del juego
game_over = False
score = 0

# Función para reiniciar el juego
def restart_game():
    global dino_rect, dino_y_speed, obstacles, game_over, score
    dino_rect.topleft = (50, HEIGHT - dino_rect.height)
    dino_y_speed = 0
    obstacles = []
    game_over = False
    score = 0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.size
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            scaled_background = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and dino_rect.bottom == HEIGHT and not game_over:
        dino_y_speed = -15

    # Aplicar gravedad
    dino_y_speed += GRAVITY
    dino_rect.y += dino_y_speed

    # Mantener al dino dentro de la pantalla
    if dino_rect.bottom > HEIGHT:
        dino_rect.bottom = HEIGHT

    # Generar obstáculos
    if random.randint(0, 100) < 10 and not game_over:
        obstacle_rect = cactus_img.get_rect()
        obstacle_rect.topleft = (WIDTH, HEIGHT - obstacle_rect.height)
        obstacles.append(obstacle_rect)

    # Mover obstáculos
    for obstacle_rect in obstacles:
        obstacle_rect.x -= 10  # Aumentar la velocidad aquí

    # Eliminar obstáculos que están fuera de la pantalla
    obstacles = [obstacle for obstacle in obstacles if obstacle.right > 0]

    # Verificar colisiones con obstáculos
    for obstacle_rect in obstacles:
        if dino_rect.colliderect(obstacle_rect):
            game_over = True

    # Renderizar
    screen.blit(scaled_background, (0, 0))
    screen.blit(dino_img, dino_rect)
    for obstacle_rect in obstacles:
        screen.blit(cactus_img, obstacle_rect)

    if game_over:
        font = pygame.font.Font(None, 36)
        text = font.render("perdiste -apretaa'R'para comenzar de nuevo", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(30)

    # Reiniciar juego si se presiona 'R'
    if game_over and keys[pygame.K_r]:
        restart_game()

pygame.quit()
git add