import pygame as p
import random
import math
from pygame import mixer

p.init()
screen = p.display.set_mode((800, 600))

mixer.music.load("./audio/background.mp3")
mixer.music.play(-1)

background = p.image.load("./images/background.png")
p.display.set_caption("Space Invaders")
p.display.set_icon(p.image.load("./images/spaceship.png"))

playerImg = p.image.load("./images/spaceship_player.png")
playerX = 368
playerY = 480
playerX_change = 0

enemyImg = list()
enemyX = list()
enemyY = list()
enemyX_change = list()
enemyY_change = list()
enemies = 10

for i in range(enemies):
    enemyImg.append(p.image.load("./images/enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(1)
    enemyY_change.append(40)

bulletImg = p.image.load("./images/bullet.png")
bulletX = playerX
bulletY = playerY
bullet_state="ready"
bulletY_change = 5

score=0
font = p.font.Font("freesansbold.ttf", 32)

textX=10
textY=10

over_font = p.font.Font("freesansbold.ttf", 64)

def show_score(x, y):
    score_disp = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_disp, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    global distance
    distance = math.sqrt(math.pow((enemyX-bulletX), 2) + math.pow((enemyY-bulletY), 2))
    if distance < 27:
        return True
    return False

running = True
while running:

    screen.fill((0, 0, 0))

    screen.blit(background, (0, 0))

    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

        if event.type == p.KEYDOWN:
            if event.key == p.K_LEFT:
                playerX_change-=2
            if event.key == p.K_RIGHT:
                playerX_change+=2
            if event.key == p.K_SPACE:
                if bullet_state == "ready":

                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == p.KEYUP:
            if event.key == p.K_LEFT or event.key == p.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >=736:
        playerX = 736
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = playerY

    for i in range(enemies):
        if enemyY[i] > 400:
            for j in range(enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = playerY
            bullet_state = "ready"
            score+=1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    show_score(textX, textY)
    p.display.update()
