import pygame
import random
import math


pygame.init()

# Display Screen Window
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

# Setting image, sound and Caption
background = pygame.image.load("C:/Users/Joshua/OneDrive/Documents/PYTHON_TESTING/(11) Pygame/Assets/background/lvl1.png")
pygame.transform.smoothscale_by(background, 10  )



pygame.display.set_caption('SHOOT PAIMON!') 

icon = pygame.image.load("C:/Users/Joshua/OneDrive/Documents/Programming Languages/PYTHON/LESSONS/(11) Pygame/cryo.ico")
pygame.display.set_icon(icon)

# optional for adding music
# mixer.music.load("")
# mixer.music.play(-1)

# GAME OVER

overfont = pygame.font.Font("freesansbold.ttf", 64)

def game_over_text(x, y):
    over_text = overfont.render("GAME OVER!", True, (225, 225, 225))
    screen.blit(over_text, (200, 250))

# PLAYER
player_image = pygame.image.load("C:/Users/Joshua/OneDrive/Documents/Programming Languages/PYTHON/LESSONS/(11) Pygame/Hilicurl.bmp")

playerX, playerY = 370, 520
playerX_change = 0

def player(x, y):
    screen.blit(player_image, (x, y))


# ENEMY
enemy_image = pygame.image.load("C:/Users/Joshua/OneDrive/Documents/Programming Languages/PYTHON/LESSONS/(11) Pygame/paimon.bmp")
enemyX = random.randint(0, 735)
enemyY = random.randint(10, 10)
enemyX_change = 0.3
enemyY_change = 10

def enemy(x, y):
    screen.blit(enemy_image, (x, y))


shield_IMG = pygame.image.load("C:/Users/Joshua/OneDrive/Documents/Programming Languages/PYTHON/LESSONS/(11) Pygame/shield.png")
shieldX = 0
shieldY = 480
shieldX_change = 0
shieldY_change = 1
shield_state = "Ready!"

def throw_shield(a, b):
    global shield_state
    shield_state = "Throw!"
    screen.blit(shield_IMG, (a + 16, b + 10))


# Collision Detection
def IsCollision(enemyX, enemyY, shieldX, shieldY):
    distance = math.sqrt((math.pow(enemyX - shieldX, 2)) + (math.pow(enemyY - shieldY, 2)))
    if distance < 27:
        return True
    else:
        return False


# SCORE
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (225, 225, 225))
    screen.blit(score, (x, y))


running = True

while running:

    screen.fill((0, 0, 0)) 
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1

        # 
            if event.key == pygame.K_SPACE:
                if shield_state is "Ready!":
                    #shield_Sound = mixer.Sound()
                    #shield_Sound.play()
                    # Get the current x coordinate of player
                    shieldX = playerX
                    throw_shield(shieldX, shieldY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    enemyX += enemyX_change

    if enemyY > 200:
        enemyY = 500
        game_over_text(10, 10)
        break

    if enemyX <= 0:
        enemyX_change = 1
    elif enemyX >= 850:
        enemyX_change = -1
        enemyY += enemyY_change


    if shieldY <= 0:
        shieldY = 480
        shieldY = "Ready!"

    if shield_state is "Throw!":
        throw_shield(shieldX, shieldY)
        shieldY -= shieldY_change


    collision = IsCollision(enemyX, enemyY, shieldX, shieldY)

    if collision:
        #explosion_Sound = mixer.Sound()
        #explosion_Sound.play()
        shieldY = 480
        shield_state = "Ready!"
        score_value += 1
        print(score_value)
        enemyX = random.randint(0, 735)
        enemyY = random.randint(10, 50)
        

    show_score(textX, textY)

    player(playerX, playerY)

    enemy(enemyX, enemyY)


    pygame.display.update() 


