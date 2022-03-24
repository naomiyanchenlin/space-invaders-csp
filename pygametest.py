import pygame
import math


# screen constants
XMODE = 800
YMODE = 600
clock = pygame.time.Clock()

# start pygame
pygame.init()
screen = pygame.display.set_mode((XMODE, YMODE))

# game images
background = pygame.image.load('space.jpg')

running = True
while running:
    clock.tick(100)
    # redraw game screen
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))