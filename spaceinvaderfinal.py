#################################################################################################
#                                    - Space Invader -                                          #
#                                                                                               #
#   Created by Naomi Lin                                                                        #
#                                                                                               #
#   Description: The defenders shoot bullets at the invaders. When shot, the invaders die. The  #
# goal is to kill all of the invaders before they reach the defender's planet.                  #
#                                                                                               #
#                                                                                               #
##################################################################################################


# import libraries
import pygame
import math


# screen constants
XMODE = 800
YMODE = 600
color_light = (170,170,170)
color_dark = (100,100,100)
white = (255,255,255)

# start pygame
pygame.init()


# game images
background = pygame.image.load('space.jpg')
invader = pygame.image.load('invaders.png')
defender = pygame.image.load('defender.png')
gameover = pygame.image.load('gameover.jpeg')
youwin = pygame.image.load('youwin.jpeg')
bullet = pygame.image.load('bullet.png')
spriteSize = (50, 50)
bulletSize = (30,30)
invaderSprite = pygame.transform.scale(invader, spriteSize)
defenderSprite = pygame.transform.scale(defender, spriteSize)
bulletSprite = pygame.transform.scale(bullet, bulletSize)

downEvent = pygame.USEREVENT + 1
bulletEvent = pygame.USEREVENT + 2
clock = pygame.time.Clock()
pygame.time.set_timer(downEvent, 1000)
pygame.time.set_timer(bulletEvent, 100)
KEYDOWN = pygame.USEREVENT + 1
clock = pygame.time.Clock()
pygame.time.set_timer(KEYDOWN, 1000)


#classes


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def moveBullet(self, deltaX, deltaY):
        self.x += deltaX
        self.y += deltaY

    def distance(self, toX, toY):
        return((toX - self.x)**2 + (toY - self.y)**2)**0.5

    def hit(self, invader):
        if self.distance(invader.x, invader.y) <=25:
            return True
        else:
            return False


class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y

    def isClicked(self, x, y):
        width = 140
        height = 40
        self.x/2 <= x <= (self.x/2 + width) and self.y/2 <= y <= (self.y/2 + height)

class Ship:
    fireRate = 3  # public variable, wait 3 seconds between firing

    def __init__(self, xVal, yVal):
        self.x = xVal
        self.y = yVal

    def moveShip(self, deltaX, deltaY):
        # conditional // use self. because it is an internal variable within Ship
        self.x += deltaX
        self.y += deltaY


class Defender(Ship):  # child funct -- has everything the parent one does but can change
    def __init__(self, x, y):
        super().__init__(x, y)
        

class Invader:
    def __init__(self, xVal, yVal):
        self.x = xVal
        self.y = yVal

    def moveInvader(self, deltaX, deltaY):
        self.x += deltaX
        self.y += deltaY


# set up screen
screen = pygame.display.set_mode((XMODE, YMODE))

# set up defender
defender = Defender(350,520)

#set up bullets
bullets = []

# set up invaders on screen
invaders = []
for i in range(0,8):
    invaders.append(Invader(30 + 100 * i, -50))
for i in range(0,7):
    invaders.append(Invader(70 + 100 * i, -150))
for i in range(0,8):
    invaders.append(Invader(30 + 100 * i, -250))

#start screen from https://www.geeksforgeeks.org/how-to-create-buttons-in-a-game-using-pygame/ and modified
smallfont = pygame.font.SysFont('Cambria',35)
textQuit = smallfont.render('quit' , True , white)
textStart = smallfont.render('start!' , True , white)
while True:
    for ev in pygame.event.get():
        if ev.type == pygame.MOUSEBUTTONDOWN:   #checks if a mouse is clicked
            if 360 <= mouse[0] <= 400 and 300 <= mouse[1] <= 340:  #if the mouse is clicked on the button the game is terminated
                break
            elif 400 <= mouse[0] <= 540 and 300 <= mouse[1] <= 340:  #if the mouse is clicked on the button the game is terminated
                pygame.quit()
                break
                  
    # fills the screen with a color
    screen.blit(background, (0, 0))
    mouse = pygame.mouse.get_pos()

    if 360 <= mouse[0] <= 400 and 300 <= mouse[1] <= 340:
        pygame.draw.rect(screen,color_light,[400,300,40,40])
          
    else:
        pygame.draw.rect(screen,color_dark,[400,300,40,40])
    screen.blit(textStart, (300,300))

    #width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40 ////// [width/2,height/2,140,40]

    # if mouse is hovered on a button it changes to lighter shade 
    if 400 <= mouse[0] <= 540 and 300 <= mouse[1] <= 340:
        pygame.draw.rect(screen,color_light,[400,300,140,40])
    elif 400 <= mouse[0] <= 540 and 300 <= mouse[1] <= 340:
        pygame.draw.rect(screen,color_light,[400,300,140,40])
          
    else:
        pygame.draw.rect(screen,color_dark,[400,300,140,40])
    screen.blit(textQuit, (450,300))
      
    # updates the frames of the game
    pygame.display.update()

# game loop
running = True
while running:
    clock.tick(40)
    # redraw game screen
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(defenderSprite, (defender.x, defender.y))
    for invader in invaders:
        screen.blit(invaderSprite, (invader.x, invader.y))
    for bullet in bullets:
        screen.blit(bulletSprite, (bullet.x, bullet.y))
    
    # input event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == downEvent:
            for invader in invaders:
                invader.moveInvader(0, 5)
            if invader.y > 250: 
                screen.blit(gameover, (0, 0))
                running = False
        elif event.type == bulletEvent:
            for bullet in bullets:
                bullet.moveBullet(0,-10)
                if bullet.y < 0:
                    bullets.remove(bullet)
                else:
                    for invader in invaders:
                        if bullet.hit(invader):
                            invaders.remove(invader)
                            bullets.remove(bullet)
                            break
            if len(invaders) == 0:
                screen.blit(youwin, (0, 0))
                running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if defender.x > 30:
                    defender.moveShip(-10,0)
            elif event.key == pygame.K_RIGHT: 
                if defender.x < 720:
                    defender.moveShip(10,0)
            elif event.key == pygame.K_SPACE:
                bullets.append(Bullet(defender.x, defender.y))   
    pygame.display.update() 








            





