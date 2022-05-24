import math
import pygame


class Enemy(object):
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.velocity = [0, 0]
        self.EToPNormalized = [0, 0]
        self.image = pygame.image.load('images/enemy.png')
        self.angle = 0
        self.speed = speed
        self.shootTime = 0
        self.bullets = []

    def update(self, playerX, playerY, cameraMovement):
        self.checkIfClose(playerX, playerY)

    def draw(self, screen):
        screen.blit(pygame.transform.rotate(self.image, self.angle), (self.x, self.y))
        self.drawBullet(screen)

    def checkIfClose(self, x, y):
        self.shootTime += 1
        enemyToPlayer = [x - self.x, y - self.y]
        if math.sqrt((enemyToPlayer[0] ** 2) + (enemyToPlayer[1] ** 2)) < 650:
            enemyToPlayerLength = math.sqrt((enemyToPlayer[0] ** 2) + (enemyToPlayer[1] ** 2))
            self.EToPNormalized = [enemyToPlayer[0] / enemyToPlayerLength, enemyToPlayer[1] / enemyToPlayerLength]
            if self.shootTime >= 200:
                self.shootTime = 0
                self.bullets.append([self.x + 25, self.y + 25, self.EToPNormalized, False])
        else:
            self.EToPNormalized = [0, 0]

        self.angle = math.degrees(math.atan2(enemyToPlayer[0], enemyToPlayer[1])) - 90

    def move(self, cameraMovementX, cameraMovementY):
        self.x += cameraMovementX
        self.y += cameraMovementY
        self.x += self.EToPNormalized[0] * self.speed
        self.y += self.EToPNormalized[1] * self.speed

    def drawBullet(self, screen):
        for bullet in self.bullets:
            bullet[0] += bullet[2][0] * 5
            bullet[1] += bullet[2][1] * 5
            pygame.draw.circle(screen, 'red', (bullet[0], bullet[1]), 5)

    def bulletRectCollide(self, rectPos, rectWidth, rectHeight):
        for i in range(len(self.bullets)):
            if self.bullets[i][3] is False:  # checks to see if bullet already hit player before
                if self.bullets[i][0] < rectPos[0] + rectWidth and self.bullets[i][0] + 10 > rectPos[0] and\
                        self.bullets[i][1] < rectPos[1] + rectHeight and self.bullets[i][1] + 10 > rectPos[1]:
                    self.bullets[i][3] = True
                    self.bullets.remove(self.bullets[i])
                    return True
        return False

