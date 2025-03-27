import pygame
import random
import math
import sys
import os

# Inicializar pygame
pygame.init()

# Configuraci�n de pantalla
screen_width = 880
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invader")

# Funci�n para obtener la ruta de los recursos
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Cargar assets
asset_background = resource_path('assets/images/background.png')
background = pygame.image.load(asset_background)

asset_icon = resource_path('assets/images/ufo.png')
icon = pygame.image.load(asset_icon)
pygame.display.set_icon(icon)

asset_sound = resource_path('assets/audios/background_music.mp3')
pygame.mixer.music.load(asset_sound)
pygame.mixer.music.set_volume(0.2)  # Volumen al 20%
pygame.mixer.music.play(-1)

asset_playerimg = resource_path('assets/images/space-invaders.png')
playerimg = pygame.image.load(asset_playerimg)

asset_bulletimg = resource_path('assets/images/bullet.png')
bulletimg = pygame.image.load(asset_bulletimg)

# ruta para la bala enemiga
asset_enemy_bullet = resource_path('assets/images/bullet4.png')
enemy_bullet_img = pygame.image.load(asset_enemy_bullet)

asset_over_font = resource_path('assets/fonts/RAVIE.TTF')
over_font = pygame.font.Font(asset_over_font, 64)

asset_font = resource_path('assets/fonts/comicbd.ttf')
font = pygame.font.Font(asset_font, 32)

clock = pygame.time.Clock()

# Variables globales del jugador
playerx = 370
playery = 470
playerx_change = 0

# Variables globales de los enemigos
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
no_of_enemies = 10

for i in range(no_of_enemies):
    enemy1_path = resource_path('assets/images/enemy1.png')
    enemyimg.append(pygame.image.load(enemy1_path))
    enemy2_path = resource_path('assets/images/enemy2.png')
    enemyimg.append(pygame.image.load(enemy2_path))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(0, 150))
    enemyx_change.append(5)
    enemyy_change.append(20)

# Variables globales de la bala del jugador y puntuaci�n
bulletx = 0
bullety = 480
bullety_change = 10
bullet_state = "ready"
score = 0

# VARIABLE Bala del enemigo
enemy_bullet_state = "ready"  # "ready" o "fire"
enemy_bullet_x = 0
enemy_bullet_y = 0
enemy_bullet_speed = 7

# ---------------------------
# Definici�n de funciones
# ---------------------------
def show_score():
    score_value = font.render("SCORE " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (10, 10))

def draw_player(x, y):
    screen.blit(playerimg, (x, y))

def draw_enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))

def enemy_fire_bullet(x, y):
    global enemy_bullet_state, enemy_bullet_x, enemy_bullet_y
    enemy_bullet_state = "fire"
    enemy_bullet_x = x
    enemy_bullet_y = y

def isCollision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    return distance < 27

def game_over_screen():
    # Muestra GAME OVER y el score en letras grandes, y espera a que se presione una tecla
    screen.fill((0, 0, 0))
    game_over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    score_text = over_font.render("Score: " + str(score), True, (255, 255, 255))
    go_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(game_over_text, go_rect)
    screen.blit(score_text, score_rect)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def reset_game():
    global playerx, playery, bulletx, bullety, bullet_state, score
    global enemyx, enemyy, enemyx_change, enemyy_change, enemy_bullet_state
    playerx = 370
    playery = 470
    bulletx = 0
    bullety = 480
    bullet_state = "ready"
    score = 0
    enemy_bullet_state = "ready"
    for i in range(no_of_enemies):
        enemyx[i] = random.randint(0, 736)
        enemyy[i] = random.randint(0, 150)
        enemyx_change[i] = 5
        enemyy_change[i] = 20

def gameloop():
    global playerx, playerx_change, bulletx, bullety, bullet_state, score
    global enemy_bullet_state, enemy_bullet_x, enemy_bullet_y
    running = True
    while running:
        # Fondo
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        
        # Manejo de eventos (disparo del jugador y cierre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletx = playerx
                        fire_bullet(bulletx, bullety)
        
        # Estado de teclas para mover al jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            playerx_change = -5
        elif keys[pygame.K_RIGHT]:
            playerx_change = 5
        else:
            playerx_change = 0
        
        # Actualizar posici�n del jugador
        playerx += playerx_change
        if playerx < 0:
            playerx = 0
        elif playerx > 736:
            playerx = 736
        
        # Procesar enemigos
        for i in range(no_of_enemies):
            if enemyy[i] > 440:
                game_over_screen()
                reset_game()
                running = False
                break
            
            enemyx[i] += enemyx_change[i]
            if enemyx[i] < 0:
                enemyx_change[i] = 5
                enemyy[i] += enemyy_change[i]
            elif enemyx[i] > 736:
                enemyx_change[i] = -5
                enemyy[i] += enemyy_change[i]
            
            # Colisi�n entre la bala del jugador y el enemigo
            if isCollision(enemyx[i], enemyy[i], bulletx, bullety):
                bullety = 480
                bullet_state = "ready"
                score += 1
                enemyx[i] = random.randint(0, 736)
                enemyy[i] = random.randint(0, 150)
            
            draw_enemy(enemyx[i], enemyy[i], i)
        
        # Oportunidad de que el enemigo 1 (�ndice 0) dispare
        if enemy_bullet_state == "ready":
            if random.random() < 1:
                enemy_fire_bullet(enemyx[0], enemyy[0])
        
        # Actualizar bala del enemigo
        if enemy_bullet_state == "fire":
            screen.blit(enemy_bullet_img, (enemy_bullet_x + 16, enemy_bullet_y + 10))
            enemy_bullet_y += enemy_bullet_speed
            if isCollision(enemy_bullet_x, enemy_bullet_y, playerx, playery):
                game_over_screen()
                reset_game()
                running = False
            if enemy_bullet_y > screen_height:
                enemy_bullet_state = "ready"
        
        # Movimiento de la bala del jugador
        if bullet_state == "fire":
            fire_bullet(bulletx, bullety)
            bullety -= bullety_change
        if bullety < 0:
            bullety = 480
            bullet_state = "ready"
        
        draw_player(playerx, playery)
        show_score()
        pygame.display.update()
        clock.tick(120)

def main_menu():
    menu = True
    while menu:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        title_text = over_font.render("SPACE INVADER", True, (255, 255, 255))
        instruction_text = font.render("Presiona ENTER para iniciar", True, (255, 255, 255))
        screen.blit(title_text, title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50)))
        screen.blit(instruction_text, instruction_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50)))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu = False

def main():
    # Bucle principal que permite reiniciar el juego tras un Game Over
    while True:
        main_menu()
        gameloop()

if __name__ == '__main__':
    main()

