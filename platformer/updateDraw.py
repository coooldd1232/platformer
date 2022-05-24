import pygame
import blocklist
from globalStuff import *
import sys
import enemyFile
import random
import time

pygame.init()

blocks.createBlocks(blocklist.blocks)
for i in range(0, 55, 1):
    blocks.list.append([i * 50, 750])
    blocks.list.append([i * 50, -50])

for i in range(0, 25, 1):
    blocks.list.append([i * 50 - 1250, -50])

enemy1 = enemyFile.Enemy(-1000, 500, (random.randint(10, 25)) / 10)
enemies = [enemy1]
gameStart = time.time()
last6Sec = time.time() - 4
last30Sec = time.time() - 30
Sec90Forward = time.time() + 90
musicChangeCheck = False
volumeOff = pygame.image.load('images/volumeOff.png')
volumeOn = pygame.image.load('images/volumeOn.png')
def Update():
    global last6Sec, last30Sec, musicChangeCheck, Sec90Forward
    mouse = pygame.mouse.get_pos()
    currentTime = time.time()
    if currentTime > Sec90Forward:
        player.apple = True
        Sec90Forward = time.time() + 90
    if currentTime - last6Sec >= 6:
        enemies.append(enemyFile.Enemy(random.randint(blocks.list[212][0], blocks.list[443][0]), random.randint(0, 800), (random.randint(10, 25)) / 10))
        last6Sec = time.time()
    if currentTime - last30Sec >= 30:
        for enemy in enemies:
            enemy.x = random.randint(blocks.list[212][0], blocks.list[443][0])
            enemy.y = random.randint(0, 800)
            enemy.speed += 0.2
        last30Sec = time.time()

    player.update(blocks, enemies)
    for enemy in enemies:
        enemy.update(player.x, player.y, [cameraMovementX, cameraMovementY])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.left = True
            if event.key == pygame.K_RIGHT:
                player.right = True
            if event.key == pygame.K_UP and player.ableToJump:
                player.jump()
                player.ableToJump = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.left = False
            if event.key == pygame.K_RIGHT:
                player.right = False
            if event.key == pygame.K_SPACE and player.apple:
                player.apple = False
                player.health = 100
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 1350 < mouse[0] < 1400 and 0 < mouse[1] < 50:
                if pygame.mixer.music.get_volume() > 0:
                    pygame.mixer.music.set_volume(0)
                elif pygame.mixer.music.get_volume() == 0:
                    pygame.mixer.music.set_volume(0.9921875)


def Draw(screen):
    screen.fill((48, 24, 0))
    player.draw(screen)
    player.drawHealthBar(screen)
    blocks.draw(screen)
    if pygame.mixer.music.get_volume() == 0:
        screen.blit(volumeOff, (1350, 0))
    else:
        screen.blit(volumeOn, (1350, 0))
    for enemy in enemies:
        enemy.draw(screen)
    pygame.display.flip()
