import pygame
import sys
import time


class Player(object):
    def __init__(self):
        self.x = 675
        self.y = 600
        self.width = 40
        self.height = 50
        self.image = pygame.image.load('images/player.png')
        self.ableToJump = True
        self.velocity = [0, 0]
        self.gravity = 1
        self.right = False
        self.left = False
        self.imageToDraw = self.image
        self.health = 100
        self.apple = False
        self.beginning = time.time()
        self.appleImage = pygame.image.load('images/magicApple.png')

    def update(self, blocks, enemies):
        self.updateVelocity()
        if self.velocity[1] > 30:
            self.velocity[1] = 30
        self.move(blocks, enemies)
        if self.health < 1:
            # scores
            print("you lose")
            yourScore = round(time.time() - self.beginning)
            readFile = open('bestScore.txt', 'r')
            bestScore = readFile.readline()
            if int(yourScore) > int(bestScore):
                print(f'YOU BEAT THE BEST SCORE AT {bestScore} seconds, AND YOU GOT {yourScore}')
                writeFile = open('bestScore.txt', 'w')
                writeFile.write(str(yourScore))
            else:
                print(f'your score: {yourScore}, best score: {bestScore}')

            readFile.close()

            pygame.quit()
            sys.exit()
        heal = True
        for enemy in enemies:
            if self.rectCollide([enemy.x, enemy.y]):
                heal = False
                self.health -= 0.7
            if enemy.bulletRectCollide([self.x, self.y], self.width, self.height):
                self.health -= 25
        if heal:
            self.health += 0.1
        if self.health > 100:
            self.health = 100

    def move(self, blocks, enemies):
        blocks.cameraBlocks(-self.velocity[0], 0)
        for enemy in enemies:
            enemy.move(-self.velocity[0], 0)
            for bullet in enemy.bullets:
                bullet[0] += -self.velocity[0]
        collisions = blocks.getCollisions(self)
        for block in collisions:  # x velocity collisions
            if self.rectCollide(block):
                if self.velocity[0] > 0:  # moving right
                    blocks.cameraBlocks(self.velocity[0], 0)
                    for enemy in enemies:
                        enemy.x += self.velocity[0]
                        for bullet in enemy.bullets:
                            bullet[0] += self.velocity[0]
                if self.velocity[0] < 0:  # moving left
                    blocks.cameraBlocks(self.velocity[0], 0)
                    for enemy in enemies:
                        enemy.x += self.velocity[0]
                        for bullet in enemy.bullets:
                            bullet[0] += self.velocity[0]
        self.y += self.velocity[1]
        collisions = blocks.getCollisions(self)
        for block in collisions:  # y velocity collisions
            if self.rectCollide(block):
                if self.velocity[1] > 0:  # moving down
                    self.velocity[1] = 0
                    self.ableToJump = True
                    self.y = block[1] - self.height
                elif self.velocity[1] < 0:  # moving up
                    self.velocity[1] = 0
                    self.y = block[1] + 50

    def jump(self):
        self.velocity[1] = -20

    def draw(self, screen):
        screen.blit(self.imageToDraw, (self.x, self.y))
        if self.apple:
            screen.blit(self.appleImage, (self.x + 15, self.y - 45))

    def rectCollide(self, rect):
        if self.x < rect[0] + 50 and self.x + self.width > rect[0] and\
                self.y < rect[1] + 50 and self.y + self.height > rect[1]:
            return True
        return False

    def updateVelocity(self):
        if self.right:
            self.velocity[0] = 7
            self.imageToDraw = self.image
        if self.left:
            self.velocity[0] = -7
            self.imageToDraw = pygame.transform.flip(self.image, True, False)
        if (self.right and self.left) or (self.right is False and self.left is False):
            self.velocity[0] = 0
        self.velocity[1] += self.gravity

    def drawHealthBar(self, screen):
        pygame.draw.rect(screen, 'green', (self.x, self.y - 25, int(self.health / 2), 20))
        pygame.draw.rect(screen, 'red', (self.x + int(self.health / 2), self.y - 25, int(50 - self.health / 2), 20))
