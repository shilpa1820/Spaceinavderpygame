import pygame
import random
import math
from pygame import mixer

# initializing pygame
pygame.init()

# creating a screen
# width height
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("background1.png")

#background
mixer.music.load("background.wav")
mixer.music.play(-1)

# title
pygame.display.set_caption("space invader")

# icon
icon = pygame.image.load("ufo2.png")
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load("spaceship.png")
playerX = 370
playerY = 500
playerX_change = 0


# is a meth to draw the -player on th screen
def player(x, y):
    screen.blit(playerimg, (x, y))


# enemy
enemyimg = []
enemyX = []
enemyY = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 100))
    enemyx_change.append(1)
    enemyy_change.append(20)

# bullet
# ready = the bulte cant be seen
# fire= bullter is gonna be seen
bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 450
bulletx_change = 0
bullety_change = 5
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

# game over
over_font = pygame.font.Font('freesansbold.ttf',100)


textx = 10
texty = 10

def show_score(x,y):
    score = font.render("score : " + str(score_value), True,(255,255,255))
    screen.blit(score , (x,y))

def game_over_txt():
    over_txt = over_font.render("GAME OVER", True,(255,0,0))
    screen.blit(over_txt , (100,250))



# this meth is to draw the enemy
def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


# meth to draw the bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


# function to check if the collusion is happen
def iscollusion(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(bulletY - enemyY, 2)))
    if distance <= 27:
        return True
    else:
        return False


# game loop
runing = True

while runing:
    # to add colour to the screen
    screen.fill((0, 150, 200))
    # background img
    screen.blit(background, (0, 0))

    # anything happening in the game is a event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False

        # if thekeystore is pressed check if  right or left
        if event.type == pygame.KEYDOWN:  # key down is pressing the key
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            # shooting the bullet
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    shootsound = mixer.Sound('laser.wav')
                    shootsound.play( )

        if event.type == pygame.KEYUP:  # key up is releasing the key
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # bullet state
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bullety_change
    # respawn the bullet
    if bulletY <= 0:
        bulletY = 450
        bullet_state = "ready"

    # checking for boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 740:
        playerX = 740

    # enemy movement
    for i in range(num_of_enemies):
        # game over
        if enemyY[i]>=200:
            for i in range(num_of_enemies):
                enemyY[i]= 2000
            game_over_txt()
            break


        if enemyX[i] <= 0:
            enemyx_change[i]= 1
            enemyY[i] += enemyy_change[i]
        elif enemyX[i]>= 740:
            enemyx_change[i] = -1
            enemyY[i] += enemyy_change[i]
        enemyX[i] += enemyx_change[i]

        # collusion
        collusion = iscollusion(enemyX[i], enemyY[i], bulletX, bulletY)
        if collusion:
          bulletY = 480
          bullet_state = "ready"
          score_value+= 1
          print(score_value)
          enemyX[i] = random.randint(0, 735)
          enemyY[i] = random.randint(0, 100)
          explsionsound = mixer.Sound('explosion.wav')
          explsionsound.play()
        enemy(enemyX[i], enemyY[i],i)

    # cal the method to draw the spaceship
    playerX += playerX_change

    player(playerX, playerY)
    show_score(textx, texty)



    # this has to be done to update the display
    pygame.display.update()
