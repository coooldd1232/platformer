import pygame
import updateDraw
import time

pygame.init()
pygame.mixer.music.load('music/Chopin - Nocturne op.9 No.2.mp3')
pygame.mixer.music.play(-1)
SCREENWIDTH = 1400
SCREENHEIGHT = 800
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('platform game i hope')
clock = pygame.time.Clock()
time30SecFuture = time.time() + 30
gameRunning = True
changeMusicCheck = False
while gameRunning:
    currentTime = time.time()
    if currentTime > time30SecFuture and changeMusicCheck is False:
        changeMusicCheck = True
        pygame.mixer.music.load('music/Jaws - Theme song.mp3')
        pygame.mixer.music.play(-1)
    if changeMusicCheck:
        pygame.mixer.music.queue('music/Beethoven - Für Elise Nightmare (Piano Solo).mp3')


    updateDraw.Update()
    updateDraw.Draw(screen)
    clock.tick(60)
