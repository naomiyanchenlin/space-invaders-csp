#############################################################################################
#                                    - Space Invader -                                      #
#
#   Created by Naomi Lin
#
#   Description:
#
#
#


# import libraries
import pygame
import math

# screen constants
XMODE = 800
YMODE = 600

# start pygame
pygame.init()

# game images
background = pygame.image.load('imgs\space.jpg')
invader = pygame.image.load('imgs\invaders.png')
defender = pygame.image.load('imgs\defender.png')

# set up screen
screen = pygame.display.set_mode((XMODE, YMODE))

# game loop
running = True
while running:
    # redraw game screen
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    # input event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def mov_to(self, deltax, deltay):
        self.x += deltax
        self.y += deltay

    def distance(self, toX, toY):
        return((self.x - toX)**2 / (self.y - toY)**2)**0.5


class Bullets:
    position = Point(0, 0)

    def __init__(self, x=0, y=0):
        self.position.x = x
        self.position.y = y

    def mov_to(self, x, y):
        self.position.mov_to(x, y)

    def distance(self, x, y):
        return self.position.distance(x, y)


testObj = Bullets()
netString = str((testObj.distance(10, 10)))
print(testObj.distance(10, 10))


class Ship:
    fireRate = 3  # public variable, wait 3 seconds between firing
    xShiftRate = 10  # move 10 pixels per shift
    yShiftRate = 20  # move 20 pixels per shift

    def __init__(self, xVal, yVal):
        self.position = Point(xVal, yVal)

    def move(self, deltaX, deltaY):
        # conditional // use self. because it is an internal variable within Ship
        if (deltaX <= self.xShiftRate and deltaY <= self.yShiftRate):
            self.position.x += deltaX
            self.position.y += deltaY


class Defender(Ship):  # child funct -- has everything the parent one does but can change
    def __init__(self, x, y, imageVal, fireVal):
        # super(). refer to parent class -- can also do pass if not change
        super().__init__(x, y, imageVal)
        super().fireRate = fireVal  # OVERRIDING!!! changing the fireRate




