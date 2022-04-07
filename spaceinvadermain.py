####################################################################################################
#                                       - Space Invader -                                          #
#                                                                                                  #
#   Created by Yanchen Lin                                                                         #
#                                                                                                  #
#   Description: The goal is to kill all of the invaders before they reach the defender's planet   #
#   The defenders shoot bullets at the invaders. When shot, the invaders die. When the meteor      #
#   randomly spawns onto the screen, the defender can touch it and it will go through and kill     #
#   two vertical columns of invaders. The defenders can also phone a friend. If they touch the     #
#   phone icon, they summon a friend that will kill a row of invaders.                             #
#                                                                                                  #
#                                                                                                  #
#                                                                                                  #
####################################################################################################


# import libraries
import pygame
import random


# screen constants
XMODE = 800
YMODE = 600
LIGHTCOLOR = (170,170,170)
DARKCOLOR = (100,100,100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


# start pygame
pygame.init()

# set up screen
screen = pygame.display.set_mode((XMODE, YMODE))

# set game images & determine sprite sizes
background = pygame.image.load('space.jpg')
invader = pygame.image.load('invaders.png')
defender = pygame.image.load('defender.png')
gameover = pygame.image.load('gameover.jpeg')
youwin = pygame.image.load('youwin.jpeg')
bullet = pygame.image.load('bullet.png')
meteor = pygame.image.load('meteor.png')
friend = pygame.image.load('friend.png')
phone = pygame.image.load('phone.png')
spriteSize = (50, 50)
bulletSize = (30, 30)
meteorSize = (85, 85)
invaderSprite = pygame.transform.scale(invader, spriteSize)
defenderSprite = pygame.transform.scale(defender, spriteSize)
friendSprite = pygame.transform.scale(friend, spriteSize)
bulletSprite = pygame.transform.scale(bullet, bulletSize)
meteorSprite = pygame.transform.scale(meteor, meteorSize)
phoneSprite = pygame.transform.scale(phone, spriteSize)

#from https://stackoverflow.com/questions/23368999/move-an-object-every-few-seconds-in-pygame and edited
#runs each event over and over again
downEvent = pygame.USEREVENT + 1
bulletEvent = pygame.USEREVENT + 2
meteorEvent = pygame.USEREVENT + 3
friendEvent = pygame.USEREVENT + 4
clock = pygame.time.Clock()
pygame.time.set_timer(downEvent, 1000)
pygame.time.set_timer(bulletEvent, 100)
pygame.time.set_timer(meteorEvent, 100)
pygame.time.set_timer(friendEvent, 100)
KEYDOWN = pygame.USEREVENT + 1
clock = pygame.time.Clock()
pygame.time.set_timer(KEYDOWN, 1000)



#classes
class Bullet:
    def __init__(self, x, y):                                               #def init finds the location
        self.x = x
        self.y = y

    def moveBullet(self, deltaX, deltaY):                                   #def move is a function that moves the object
        self.x += deltaX
        self.y += deltaY

    def distance(self, toX, toY):                                           #def distance finds the distance between two objects
        return((toX - self.x)**2 + (toY - self.y)**2)**0.5

    def hit(self, invader):                                                 #def hit checks if the object touches another object
        if self.distance(invader.x, invader.y) <=25:
            return True
        else:
            return False

class Meteor:
    def __init__(self, x, y):                                               #active --> is a state where object is moving 
        self.x = x
        self.y = y
        self.active = False

    def moveMeteor(self, deltaX, deltaY):
        self.x += deltaX
        self.y += deltaY

    def distance(self, toX, toY):
        return((toX - self.x)**2 + (toY - self.y)**2)**0.5

    def getPower(self, defender):                                           #getPower checks whether the defender touches the initiator 
        if self.distance(defender.x, defender.y) <=85:                      #object that starts the power up tool (meteor/friend)
            return True
        else:
            return False

    def hit(self, invader):
        if self.distance(invader.x, invader.y) <=85:
            return True
        else:
            return False

class Friend:                                                         
    def __init__(self, x, y):                                        
        self.x = x
        self.y = y
        self.active = False

    def moveFriend(self, deltaX, deltaY):                            
        self.x += deltaX
        self.y += deltaY

    def distance(self, toX, toY):
        return((toX - self.x)**2 + (toY - self.y)**2)**0.5

    def hit(self, invader):                    
        if self.distance(invader.x, invader.y) <=25:
            return True
        else:
            return False

class Phone:                                                         
    def __init__(self, x, y):                                      
        self.x = x
        self.y = y
        self.active = False

    def distance(self, toX, toY):
        return((toX - self.x)**2 + (toY - self.y)**2)**0.5

    def getPower(self, defender):
        if self.distance(defender.x, defender.y) <=25:
            return True
        else:
            return False

class Button:                                                                  #common button, with text and regulated size
    def __init__(self, text, x, y):
        self.text = text
        self.width = 140
        self.height = 40
        self.x = x
        self.y = y


class Ship:
    fireRate = 3  # public variable, wait 3 seconds between firing

    def __init__(self, xVal, yVal):
        self.x = xVal
        self.y = yVal

    def moveShip(self, deltaX, deltaY):    # conditional // use self. because it is an internal variable within Ship
        self.x += deltaX
        self.y += deltaY


class Defender(Ship):  # child funct -- has everything the parent one does but can change
    def __init__(self, x, y):
        super().__init__(x, y)
        
class Invader(Ship):
    def __init__(self, x, y):
        super().__init__(x, y)



# set up defender
defender = Defender(350,520)

#set up bullets
bullets = []

#set up meteors
meteors = []
meteorShown = False

#set up friend
friends = []            

#set up phone and whether phone has been used yet
phones = []
phoneShown = False

# set up the rows of invaders
invaders = []
for i in range(0,8):
    invaders.append(Invader(30 + 100 * i, -50))
for i in range(0,7):
    invaders.append(Invader(70 + 100 * i, -150))
for i in range(0,8):
    invaders.append(Invader(30 + 100 * i, -250))



#start screen from https://www.geeksforgeeks.org/how-to-create-buttons-in-a-game-using-pygame/ and modified
smallfont = pygame.font.SysFont('Cambria',35)
textQuit = smallfont.render('quit' , True , WHITE)
textStart = smallfont.render('start!' , True , WHITE)
textRules = smallfont.render('rules' , True , WHITE)
startButton = Button(textStart, 220, 300)
quitButton = Button(textQuit, 460, 300)
rulesButton = Button(textRules, 340, 400)
#rules page from http://programarcadegames.com/python_examples/f.php?file=instruction_screen.py and modified
rulesFont = pygame.font.SysFont('Cambria', 30)
rulesTitle = pygame.font.SysFont('Cambria', 60, italic = True)
subTitle = pygame.font.SysFont('Cambria', 35)
quit2Button = Button(textQuit, 460, 500)
textBack = smallfont.render('back' , True , WHITE)



#game loop
running = True
START = 0                                                   #creating different gameStates
RULES = 1
INGAME = 2
gameState = START
while running:
    clock.tick(40)                                          #40 frames per minute
    screen.blit(background, (0, 0))                         #put the background on the screen 


    if gameState == INGAME:                                 #INGAME is during the actual game 
        #spawn invaders
        screen.blit(defenderSprite, (defender.x, defender.y))           #put the sprites onto the screen or where they would be
        for invader in invaders:
            screen.blit(invaderSprite, (invader.x, invader.y))
        for bullet in bullets:
            screen.blit(bulletSprite, (bullet.x, bullet.y))
        for meteor in meteors:
            screen.blit(meteorSprite, (meteor.x, meteor.y))
        
        # code for random range from https://stackoverflow.com/questions/34240564/python-pygame-spawning-at-random-time and edited  
        # if the meteor has not been used yet during this game, once the programs' randomly selected number is 1, which is at a random 
        # time, the meteor will spawn at a random locations and the meteorShown will change to true, so this will not run again
        if meteorShown == False:
            if random.randrange(1,2500) == 1:
                meteorShown = True
                meteors.append(Meteor(random.randrange(50, 750), 500))
        
        if phoneShown == False:                               
            if random.randrange(1,2500) == 1:                 
                phoneShown = True
                phones.append(Phone(random.randrange(50, 750), 500))
        

        # input event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == downEvent:                           # when it is downEvent, the invaders move down the screen
                for invader in invaders:                            # if the invaders reach the bottom of the screen, gameover
                    invader.moveShip(0, 5)
                if invader.y > 250: 
                    screen.blit(gameover, (0, 0))
                    running = False

            elif event.type == bulletEvent:                         # when it is bulletEvent, the bullets move up at a constant speed
                for bullet in bullets:                              # if the bullet hits an invader, they both disappear
                    bullet.moveBullet(0,-10)                        # if the bullets reach the top of the screen, they disappear
                    if bullet.y < 0:                                # if there are no invaders, which you can find by checking the 
                        bullets.remove(bullet)                      # length of the array you win and return to start screen
                    else:
                        for invader in invaders:
                            if bullet.hit(invader):
                                invaders.remove(invader)
                                bullets.remove(bullet)
                                break
                if len(invaders) == 0:
                    screen.blit(youwin, (0, 0))
                    gameState = START

            elif event.type == meteorEvent:                                 # during meteorEvent, if meteor.active is True, meaning that
                for meteor in meteors:                                      # the defender touched the meteor, then it moves up. unlike the
                    if meteor.active == True:                               # bullet, when the meteor touches the invader, it doesn't disappear
                        meteor.moveMeteor(0,-10)                            # only the invader disappears, so it can kill a whole column of invaders
                        if meteor.y < 0:
                            meteors.remove(meteor)
                        else:
                            for invader in invaders:
                                if meteor.hit(invader):
                                    invaders.remove(invader)
                                    break
            
            elif event.type == friendEvent:                                  #if friend is on screen after the defender touches
                for friend in friends:                                       #the phone, then the friend moves right, if it hits 
                    if friend.active == True:                                #invaders, they disappear and the friend only disappears
                        friend.moveFriend(10,0)                              #when it reaches the edge of the screen
                        if friend.x > 800:
                            friends.remove(friend)
                        else:
                            for invader in invaders:
                                if friend.hit(invader):
                                    invaders.remove(invader)
                                    break
 

            #code from https://opensource.com/article/17/12/game-python-moving-player and edited
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:                             # if the left key is moved, the defender moves left but is limited to 30
                    if defender.x > 30:                                    # so it does not go off the screen
                        defender.moveShip(-10,0)
                        for meteor in meteors:                             #for the meteor, if the defender touches it, it sets getPower to True
                            if meteor.getPower(defender):                  # which sets meteor.active to true so it begins moving
                                meteor.active = True
                        for phone in phones:                               #for the phone, if it touches the defender, the friend will
                            if phone.getPower(defender):                   #spawn onto the screen on the side
                                friend.active = True
                                friends.append(Friend(25, 100))
                elif event.key == pygame.K_RIGHT:                           # same thing as left
                    if defender.x < 720:                                    # the for loops are used here to check whether the defender has touched the
                        defender.moveShip(10,0)                             # object yet because the first time they will touch is when the defender moves
                        for meteor in meteors:                              # to touch it
                            if meteor.getPower(defender):
                                meteor.active = True
                        for phone in phones:
                            if phone.getPower(defender):
                                friend.active = True
                                friends.append(Friend(25, 100))    
                elif event.key == pygame.K_SPACE:
                    bullets.append(Bullet(defender.x, defender.y))          # if the space key is pressed, a bullet is spawned at the defender's location



    #start screen from https://www.geeksforgeeks.org/how-to-create-buttons-in-a-game-using-pygame/ and modified
    elif gameState == START:
        mouse = pygame.mouse.get_pos() 
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:     #if the mouse is clicked, check which button the mouse is above
                if startButton.x <= mouse[0] <= (startButton.x + startButton.width) and startButton.y <= mouse[1] <= (startButton.y + startButton.height):  #if the mouse is clicked on the button the game is started
                    gameState = INGAME 
                elif quitButton.x <= mouse[0] <= (quitButton.x + quitButton.width) and quitButton.y <= mouse[1] <= (quitButton.y + quitButton.height):  #if the mouse is clicked on the button the game is terminated
                    pygame.quit()
                elif rulesButton.x <= mouse[0] <= (rulesButton.x + rulesButton.width) and rulesButton.y <= mouse[1] <= (rulesButton.y + rulesButton.height):  #if the mouse is clicked on the button the game is terminated
                    gameState = RULES

        #if the mouse is on the button, the color is light. if not, the color is dark
        if (startButton.x - 35) <= mouse[0] <= (startButton.x + startButton.width) and startButton.y <= mouse[1] <= (startButton.y + startButton.height):  #if the mouse is clicked on the button the game is started
            pygame.draw.rect(screen, LIGHTCOLOR, [(startButton.x - (35)), startButton.y, startButton.width, startButton.height])
        else:
            pygame.draw.rect(screen, DARKCOLOR, [(startButton.x - (35)), startButton.y, startButton.width, startButton.height])
        
        if (quitButton.x - 35) <= mouse[0] <= (quitButton.x + quitButton.width) and quitButton.y <= mouse[1] <= (quitButton.y + quitButton.height):  #if the mouse is clicked on the button the game is started
            pygame.draw.rect(screen, LIGHTCOLOR, [(quitButton.x - (35)), quitButton.y, quitButton.width, quitButton.height])
        else:
            pygame.draw.rect(screen, DARKCOLOR, [(quitButton.x - (35)), quitButton.y, quitButton.width, quitButton.height])

        if (rulesButton.x - 35) <= mouse[0] <= (rulesButton.x + quitButton.width) and rulesButton.y <= mouse[1] <= (rulesButton.y + rulesButton.height):  #if the mouse is clicked on the button the game is started
            pygame.draw.rect(screen, LIGHTCOLOR, [(rulesButton.x - (35)), rulesButton.y, rulesButton.width, rulesButton.height])
        else:
            pygame.draw.rect(screen, DARKCOLOR, [(rulesButton.x - (35)), rulesButton.y, rulesButton.width, rulesButton.height])

        #putting the text onto the buttons
        screen.blit(textStart, (startButton.x, startButton.y))
        screen.blit(textQuit, (quitButton.x, quitButton.y))
        screen.blit(textRules, (rulesButton.x, rulesButton.y))


    #rules page from http://programarcadegames.com/python_examples/f.php?file=instruction_screen.py and modified
    elif gameState == RULES:
        text = rulesTitle.render("Instructions", True, WHITE)
        screen.blit(text, [10, 20])
        text = subTitle.render("You are a defending your planet from space invaders.", True, GREEN)
        screen.blit(text, [10, 70])
        text = rulesFont.render("1. Use the left and right arrows to move.", True, WHITE)
        screen.blit(text, [150, 160])
        text = rulesFont.render("2. Use the space bar to shoot.", True, WHITE)
        screen.blit(text, [150, 190])
        text = rulesFont.render("3. If you touch the meteor, it will", True, WHITE)
        screen.blit(text, [150, 220])
        text = rulesFont.render("kill a vertical column of invaders.", True, WHITE)
        screen.blit(text, [150, 250])
        text = rulesFont.render("4. If you touch the cell phone, you can", True, WHITE)
        screen.blit(text, [150, 280])
        text = rulesFont.render("call a fellow defender to kill a whole", True, WHITE)
        screen.blit(text, [150, 310])
        text = rulesFont.render("hortizontal row of invaders.", True, WHITE)
        screen.blit(text, [150, 340])
        mouse = pygame.mouse.get_pos() 
        for ev in pygame.event.get():       #same button code
            if ev.type == pygame.MOUSEBUTTONDOWN: 
                if quit2Button.x <= mouse[0] <= (quit2Button.x + quit2Button.width) and quit2Button.y <= mouse[1] <= (quit2Button.y + quit2Button.height):  #if the mouse is clicked on the button the game is terminated
                    gameState = START
        if (quit2Button.x - 35) <= mouse[0] <= (quit2Button.x + quit2Button.width) and quit2Button.y <= mouse[1] <= (quit2Button.y + quit2Button.height):  #if the mouse is clicked on the button the game is started
            pygame.draw.rect(screen, LIGHTCOLOR, [(quit2Button.x - (35)), quit2Button.y, quit2Button.width, quit2Button.height])
        else:
            pygame.draw.rect(screen, DARKCOLOR, [(quit2Button.x - (35)), quit2Button.y, quit2Button.width, quit2Button.height])
        screen.blit(textBack, (quit2Button.x, quit2Button.y))


    pygame.display.update() 





            





