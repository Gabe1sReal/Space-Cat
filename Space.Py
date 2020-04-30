import pygame
import random
import math
import time

# from pygame import mixer

# Initialize the Pygame
pygame.init()

# Makes screen
screen = pygame.display.set_mode((800, 600))
background = pygame.transform.scale(pygame.image.load('background.jpg'), (800, 600))

# Sound
# -1 in play makes it play forever
# mixer.music.load()
# mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Cat")
icon = pygame.image.load('moon.png')
pygame.display.set_icon(icon)
score = 0
round = 1
round_win = False
roundX = 650
roundY = 10

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
player_changeX = 5
player_changeY = 5
lives_num = 3
livesX = 10
livesY = 50

# Enemy
number_of_enemies = 2
enemyImg = []
enemyX = []
enemyY = []
enemy_changeX = []
enemy_changeY = []
enemy_dead = 0
num_dead = 2

for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 300))
    enemy_changeX.append(3)
    enemy_changeY.append(3)
# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 0
bullet_changeX = 0
bullet_changeY = 6
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


def show_text(x, y, roundX, roundY, livesX, livesY):
    score = font.render("Score: " + str(score_value), 1, (255, 255, 255))
    round_num = font.render("Round: " + str(round), 1, (255, 255, 255))
    screen.blit(score, (x, y))
    screen.blit(round_num, (roundX, roundY))
    lives = font.render("Lives: " + str(lives_num), 1, (255, 255, 255))
    screen.blit(lives, (livesX, livesY))


def game_over(x, y):
    end = font.render("GAME OVER", 1, (255, 0, 0))
    screen.blit(end, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y - 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 28:
        return True
    else:
        return False


def playerCollision(enemyX, enemyY, playerX, playerY):
    distance = math.sqrt(math.pow(enemyX - playerX, 2) + math.pow(enemyY - playerY, 2))
    if distance < 35:
        return True
    else:
        return False


def respawn(enemyX, enemyY, playerX, playerY):
    distance = math.sqrt(math.pow(enemyX - playerX, 2) + math.pow(enemyY - playerY, 2))
    if distance >= 200:
        return True
    else:
        return False


clock = pygame.time.Clock()

# Game Loop
running = True
while running:
    pos = pygame.mouse.get_pos()
    FPS = 60
    clock.tick(FPS)
    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        playerX -= player_changeX
    if keys[pygame.K_d]:
        playerX += player_changeX
    if keys[pygame.K_w]:
        playerY -= player_changeY
    if keys[pygame.K_s]:
        playerY += player_changeY
    if keys[pygame.K_SPACE]:
        if bullet_state == "ready":
            bulletX = playerX
            bulletY = playerY
            fire_bullet(bulletX, bulletY)
    # Is giving boundaries for the player
    if playerX <= 0 and playerY <= 0 and playerX != -300:
        playerX = 0
        playerY = 0
    elif playerX <= 0 and playerY >= 536 and playerX != -300:
        playerX = 0
        playerY = 536
    elif playerX >= 736 and playerY <= 0 and playerX != -300:
        playerX = 736
        playerY = 0
    elif playerX >= 736 and playerY >= 536 and playerX != -300:
        playerX = 736
        playerY = 536
    elif playerX < 0 and playerX != -300:
        playerX = 0
    elif playerX > 736 and playerX != -300:
        playerX = 736
    elif playerY > 536 and playerX != -300:
        playerY = 536
    elif playerY < 0 and playerX != -300:
        playerY = 0

    # Bullet movement
    if bulletY <= 0:
        bulletY = -100
        bulletX = -100
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bullet_changeY
    # Enemy Movement
    for i in range(number_of_enemies):
        enemyX[i] += enemy_changeX[i]
        enemyY[i] += enemy_changeY[i]
        if enemyX[i] <= 0 and enemyX[i] != -200:
            enemy_changeX[i] = -1 * enemy_changeX[i]
        elif enemyX[i] >= 736 and enemyX[i] != -200:
            enemy_changeX[i] = -1 * enemy_changeX[i]
        elif enemyY[i] >= 534 and enemyY[i] != -200:
            enemy_changeY[i] = -1 * enemy_changeY[i]
        elif enemyY[i] <= 0 and enemyY[i] != -200:
            enemy_changeY[i] = -1 * enemy_changeY[i]

        # Collision

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        death = playerCollision(enemyX[i], enemyY[i], playerX, playerY)
        revive = respawn(enemyX[i], enemyY[i], 370, 480)
        if death:
            player_changeX = 0
            player_changeY = 0
            playerX = -300
            playerY = -300
        if revive and playerX == -300:
            playerX = 370
            playerY = 480
            player_changeX = 5
            player_changeY = 5
            lives_num -= 1

        if lives_num <= 0:
            lives_num = 0
            enemyX[i] = -200
            enemyY[i] = -200
            playerX = -300
            playerY = -300
            game_over(300, 300)
        if collision:
            bulletY = 0
            bullet_state = "ready"
            enemy_dead += 1
            if enemy_dead == num_dead:
                round_win = True
                enemy_dead = 0
                round += 1
            enemyX[i] = -200
            enemyY[i] = -200
            enemy_changeX[i] = 0
            enemy_changeY[i] = 0
            score_value += 10

        if round_win:
            round_win = False
            playerX = 370
            playerY = 480
            number_of_enemies += 1
            num_dead += 1
            for i in range(number_of_enemies):
                enemyImg.append(pygame.image.load('ufo.png'))
                enemyX.append(random.randint(0, 736))
                enemyY.append(random.randint(0, 300))
                enemy_changeX.append(0)
                enemy_changeY.append(0)
            for i in range(number_of_enemies):
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(0, 300)
                enemy_changeX[i] = random.randint(-6, 6)
                enemy_changeY[i] = random.randint(-4, 4)

        enemy(enemyX[i], enemyY[i], i)
    # Gives the player movement
    # playerX += player_changeX
    # playerY += player_changeY

    show_text(textX, textY, roundX, roundY, livesX, livesY)
    player(playerX, playerY)
    pygame.display.update()
