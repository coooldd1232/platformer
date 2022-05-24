import pygame


class Blocks(object):
    def __init__(self):
        self.list = []
        self.width = 50
        self.height = 50
        self.rendercount = 0

    def createBlocks(self, blockPosList):
        self.list = blockPosList

    def draw(self, screen):
        renderBlocks = self.getBlocksToRender()

        for block in renderBlocks:
            pygame.draw.rect(screen, (255, 255, 255), (block[0], block[1], 50, 50))

    def getCollisions(self, player):
        collisions = []
        for block in self.list:
            if player.rectCollide(block):
                collisions.append(block)
        return collisions

    def getBlocksToRender(self):
        renderBlocks = []
        for block in self.list:
            if -150 < block[0] < 1500 and -150 < block[1] < 900:
                renderBlocks.append(block)
        return self.list

    def cameraBlocks(self, cameraMovementX, cameraMovementY):
        for block in self.list:
            block[0] += cameraMovementX
            block[1] += cameraMovementY