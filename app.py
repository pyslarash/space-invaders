import math
import random
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('./img/background.png')

# Sound
mixer.music.load('./sound/background.wav')
mixer.music.play(-1)

# Caption and icon
pygame.display.set_caption('Space Invader')
icon = pygame.image.load('./img/ufo.png')
pygame.display.set_icon(icon)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Player
playerImg = pygame.image.load('./img/player.png')
playerX = 370  # X position
playerY = 480  # Y position
playerX_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))
    
# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('./img/enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)
    
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))
    

# This function shows the score
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
    
# Bullet

# Ready: You can't see the bullet on the screen
# Fire: The bullet is currently moving

bulletImg = pygame.image.load("./img/bullet.png")
bulletX = 0
bulletY = 0
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
    
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def set_background():
    global background
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))  # Corrected fill function

    # Background Image
    screen.blit(background, (0, 0))    

# Game loop
running = True
while running:
    set_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Corrected event type
            running = False
        
        # If eystroke is pressed check whether right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound('./sound/laser.wav')
                    bulletSound.play()
                    # Get the current X coordinate of a spaceship
                    bulletX = playerX # In the beginning the horizontal bullet position is equal to the player position
                    fire_bullet(bulletX, bulletY)
                    
            # If the key is released, we want to stop mooving
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                    
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736
                            
    # Enemy Movement
    for i in range(num_of_enemies):
        
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY_change[i] += enemyY_change[i]
        
        enemy(enemyX[i], enemyY[i], i)
    
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("./sound/explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
        
    # Firing bullets
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
        
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()