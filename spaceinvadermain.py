####################################################################################################
#                                       - Space Invader -                                          #
#                                                                                                  #
#                                                                                                  #
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
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


# start pygame
pygame.init()


# set up screen
screen = pygame.display.set_mode((XMODE, YMODE))


# set game images 
background = pygame.image.load('space.jpg')       #https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.cnn.com%2Fspecials%2Fspace-science&psig=AOvVaw3Gl4s4KaCS7AhkUJ1MvU1Z&ust=1650236104505000&source=images&cd=vfe&ved=0CAwQjRxqFwoTCOj-p9jWmfcCFQAAAAAdAAAAABAD
invader = pygame.image.load('invaders.png')       #https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.godisageek.com%2F2020%2F06%2Fspace-invaders-invincible-collection-is-landing-soon%2F&psig=AOvVaw1t3uaT-QurjcColIMdZMMR&ust=1650235763496000&source=images&cd=vfe&ved=0CAwQjRxqFwoTCNjZtbbVmfcCFQAAAAAdAAAAABAJ
defender = pygame.image.load('defender.png')      #https://www.google.com/url?sa=i&url=https%3A%2F%2Ffavpng.com%2Fpng_view%2Fsprite-spaceshiptwo-spacecraft-sprite-spaceshipone-png%2FrSfVm3nH&psig=AOvVaw2Rsv2KavKEVIT8gpTNgT2t&ust=1650235845333000&source=images&cd=vfe&ved=0CAwQjRxqFwoTCNip0NzVmfcCFQAAAAAdAAAAABAD
gameover = pygame.image.load('gameover.jpeg')     #https://www.google.com/url?sa=i&url=https%3A%2F%2Ftwitter.com%2Fgame_over_ports&psig=AOvVaw3TbfWu_3nAYjq7Xim29D94&ust=1650233620465000&source=images&cd=vfe&ved=0CAwQjRxqFwoTCMCg5rfNmfcCFQAAAAAdAAAAABAx
youwin = pygame.image.load('youwin.jpeg')         #https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.istockphoto.com%2Fvector%2Fpixel-art-8-bit-you-win-text-with-three-winner-golden-cups-on-black-background-gm1268272329-372239713&psig=AOvVaw1NeGLM2WM0srX7_m0V_Czq&ust=1650236140364000&source=images&cd=vfe&ved=0CAwQjRxqFwoTCKD5xe3WmfcCFQAAAAAdAAAAABAD
bullet = pygame.image.load('bullet.png')          #https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pixilart.com%2Fart%2Fgame-jam-blaster-bullet-3f235aba10b1e8f&psig=AOvVaw3pMXjFrzuVplbwJPN8SWvr&ust=1650236193725000&source=images&cd=vfe&ved=0CAwQjRxqFwoTCJCL5ILXmfcCFQAAAAAdAAAAABAD
meteor = pygame.image.load('meteor.png')          #https://www.kindpng.com/imgv/bbbixx_fireball-clipart-8-bit-8-bit-fireball-hd/
friend = pygame.image.load('friend.png')          #defender, but edited in photos app
phone = pygame.image.load('phone.png')            #https://www.vexels.com/png-svg/preview/246281/phone-pixel-art


# determine sprite sizes
pageSize = (800, 600)
spriteSize = (50, 50)
bulletSize = (30, 30)
meteorSize = (85, 85)
invaderSprite = pygame.transform.scale(invader, spriteSize)
defenderSprite = pygame.transform.scale(defender, spriteSize)
friendSprite = pygame.transform.scale(friend, spriteSize)
bulletSprite = pygame.transform.scale(bullet, bulletSize)
meteorSprite = pygame.transform.scale(meteor, meteorSize)
phoneSprite = pygame.transform.scale(phone, spriteSize)
backgroundSize = pygame.transform.scale(background, pageSize)
youwinSize = pygame.transform.scale(youwin, pageSize)
gameoverSize = pygame.transform.scale(gameover, pageSize)


# from https://stackoverflow.com/questions/23368999/move-an-object-every-few-seconds-in-pygame and edited
# runs each event over and over again
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


# declarations
meteorShown = False
phoneShown = False


# classes
class Ship:
    # wait 3 seconds between firing
    fireRate = 3  
    def __init__(self, xVal, yVal):
        self.x = xVal
        self.y = yVal
    # conditional // use self. because it is an internal variable within Ship
    def moveShip(self, deltaX, deltaY):    
        self.x += deltaX
        self.y += deltaY

## child funct -- has everything the parent one does but can change
class Defender(Ship):  
    def __init__(self, x, y):
        super().__init__(x, y)
        
class Invader(Ship):
    def __init__(self, x, y):
        super().__init__(x, y)

class Bullet:
    #init function finds the location
    def __init__(self, x, y):                                               
        self.x = x
        self.y = y
    #move is a function that moves the object
    def moveBullet(self, deltaX, deltaY):                                   
        self.x += deltaX
        self.y += deltaY
    #distance function finds the distance between two objects
    def distance(self, toX, toY):                                           
        return((toX - self.x)**2 + (toY - self.y)**2)**0.5
    #hit function checks if the object touches another object
    def hit(self, invader):                                                 
        if self.distance(invader.x, invader.y) <=25:
            return True
        else:
            return False

class Meteor:
    def __init__(self, x, y):                                               
        self.x = x
        self.y = y
        #active --> is a state where object is moving 
        self.active = False
    def moveMeteor(self, deltaX, deltaY):
        self.x += deltaX
        self.y += deltaY
    def distance(self, toX, toY):
        return((toX - self.x)**2 + (toY - self.y)**2)**0.5
    #getPower checks whether the defender touches the object that starts the power up tool (meteor/friend)
    def getPower(self, defender):                                           
        if self.distance(defender.x, defender.y) <=85:                      
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
        if self.distance(invader.x, invader.y) <=50:
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
        if self.distance(defender.x, defender.y) <=50:
            return True
        else:
            return False

## common button, with text and regulated size
class Button:                                                                  
    def __init__(self, text, x, y):
        self.text = text
        self.width = 140
        self.height = 40
        self.x = x
        self.y = y


#functions
def spriteBlit():
    #spawn invaders
    screen.blit(defenderSprite, (defender.x, defender.y))           
    for invader in invaders:
        screen.blit(invaderSprite, (invader.x, invader.y))
    for bullet in bullets:
        screen.blit(bulletSprite, (bullet.x, bullet.y))
    for meteor in meteors:
        screen.blit(meteorSprite, (meteor.x, meteor.y))
    for phone in phones:
        screen.blit(phoneSprite, (phone.x, phone.y))
    for friend in friends:
        screen.blit(friendSprite, (friend.x, friend.y))

## blit the sprites that appear at random times
def randomBlit(meteors, phones):
    global meteorShown
    global phoneShown
    # code for random range from https://stackoverflow.com/questions/34240564/python-pygame-spawning-at-random-time and edited  
    if meteorShown == False:
        # if the meteor has not been used yet during this game, once the programs' randomly selected number is 1, which is at a random time
        if random.randrange(1,2000) == 1:
            meteorShown = True
            # the meteor will spawn at a random locations and the meteorShown will change to true, so it will only spawn once
            meteors.append(Meteor(random.randrange(100, 700), 500))
        
    if phoneShown == False:                               
        if random.randrange(1,2000) == 1:                 
            phoneShown = True
            phones.append(Phone(random.randrange(50, 750), 515))

def handleDownEvent(invaders):
    for invader in invaders: 
        global gameState                                   
        invader.moveShip(0, 5)
        # if the invaders reach the bottom of the screen, gameover
        if invader.y > 550: 
            gameState = LOSE

def handleBulletEvent(bullets, invaders):
    for bullet in bullets:                              
        bullet.moveBullet(0,-10)                       
        # if the bullets reach the top of the screen, they disappear
        if bullet.y < 0:                                
            bullets.remove(bullet)                     
        else:
            for invader in invaders:
                # if the bullet hits an invader, they both disappear
                if bullet.hit(invader): 
                    invaders.remove(invader)
                    bullets.remove(bullet)
                    break
                 # if there are no invaders, go to win screen
            if len(invaders) == 0:
                global gameState
                gameState = WIN

def handleMeteorEvent(meteors, invaders):
    for meteor in meteors:                                      
        # the defender touched the meteor, meteor moves up.
        if meteor.active == True:                               
            meteor.moveMeteor(0,-10)                            
            if meteor.y < 0:
                meteors.remove(meteor)
            else:
                # when the meteor touches the invader, it doesn't disappear, only the invader disappears, so it can kill a whole column of invaders
                for invader in invaders:
                    if meteor.hit(invader):
                        invaders.remove(invader)
                        break

def handleFriendEvent(friends, invaders):
    for friend in friends:                                     
        # friend moves horizontally 
        friend.moveFriend(10,0)
        # friend disappears when it reaches the edge of the screen                              
        if friend.x > 800:                                       
            friends.remove(friend)
        else:
            # when the friend hits the invaders, the invaders disappear
            for invader in invaders:
                if friend.hit(invader):
                    invaders.remove(invader)
                    break    

def handleLeftKey(defender, meteors, phones, friends):
    # so it does not go off the screen
    if defender.x > 30:                                    
        defender.moveShip(-10,0)
        #for the meteor, if the defender touches it, it sets getPower to True, which sets meteor.active to true so it begins moving
        for meteor in meteors:                             
            if meteor.getPower(defender):                
                meteor.active = True
        # if the defender touches the phone, the phone will "call" the friend and it will spawn onto the screen on the side  
        for phone in phones:                               
            if phone.getPower(defender):
                phones.remove(phone)                                         
                friends.append(Friend(25, 100)) 

def handleRightKey(defender, meteors, phones, friends):
    if defender.x < 720: 
        defender.moveShip(10,0) 
        # for loops check whether the defender touched the object yet because the first time they will touch is when the defender moves                            
        for meteor in meteors:                              
            if meteor.getPower(defender):
                meteor.active = True
        for phone in phones:
            if phone.getPower(defender):
                phones.remove(phone)   
                friends.append(Friend(25, 100))  


# set up defender
defender = Defender(350,520)

#set up bullets
bullets = []

#set up meteors
meteors = []

#set up friend
friends = []            

#set up phone and whether phone has been used yet
phones = []

# set up the rows of invaders
invaders = []
for i in range(0,8):
    invaders.append(Invader(30 + 100 * i, -50))
for i in range(0,7):
    invaders.append(Invader(70 + 100 * i, -150))
for i in range(0,8):
    invaders.append(Invader(30 + 100 * i, -250))


# start screen from https://www.geeksforgeeks.org/how-to-create-buttons-in-a-game-using-pygame/ and modified
smallfont = pygame.font.SysFont('Cambria',35)
textQuit = smallfont.render('quit' , True , WHITE)
textStart = smallfont.render('start!' , True , WHITE)
textRules = smallfont.render('rules' , True , WHITE)
startButton = Button(textStart, 220, 300)
quitButton = Button(textQuit, 460, 300)
rulesButton = Button(textRules, 340, 400)
## rules page from http://programarcadegames.com/python_examples/f.php?file=instruction_screen.py and modified
rulesFont = pygame.font.SysFont('Cambria', 30)
rulesTitle = pygame.font.SysFont('Cambria', 60, italic = True)
subTitle = pygame.font.SysFont('Cambria', 35)
quit2Button = Button(textQuit, 460, 500)
textBack = smallfont.render('home' , True , WHITE)


## creating different gameStates
START = 0                                                   
RULES = 1
INGAME = 2
WIN = 3
LOSE = 4
gameState = START


# game loop 
running = True
endcounter = 0

while running:
    #40 frames per minute
    clock.tick(40)                                          
    screen.blit(backgroundSize, (0, 0))                        


    #start screen from https://www.geeksforgeeks.org/how-to-create-buttons-in-a-game-using-pygame/ and modified
    if gameState == START:
        mouse = pygame.mouse.get_pos() 
        for ev in pygame.event.get():
            #if the mouse is clicked, check which button the mouse is above
            if ev.type == pygame.MOUSEBUTTONDOWN:    
                #if the mouse is clicked on the button the game is started 
                if startButton.x <= mouse[0] <= (startButton.x + startButton.width) and startButton.y <= mouse[1] <= (startButton.y + startButton.height):  
                    gameState = INGAME 
                #if the mouse is clicked on the button the game is terminated
                elif quitButton.x <= mouse[0] <= (quitButton.x + quitButton.width) and quitButton.y <= mouse[1] <= (quitButton.y + quitButton.height):  
                    pygame.quit()
                #if the mouse is clicked on the button, move to rules page
                elif rulesButton.x <= mouse[0] <= (rulesButton.x + rulesButton.width) and rulesButton.y <= mouse[1] <= (rulesButton.y + rulesButton.height):  
                    gameState = RULES
        #if the mouse is on the button, the color is light. if not, the color is dark
        if (startButton.x - 35) <= mouse[0] <= (startButton.x + startButton.width) and startButton.y <= mouse[1] <= (startButton.y + startButton.height): 
            pygame.draw.rect(screen, LIGHTCOLOR, [(startButton.x - (35)), startButton.y, startButton.width, startButton.height])
        else:
            pygame.draw.rect(screen, DARKCOLOR, [(startButton.x - (35)), startButton.y, startButton.width, startButton.height])
        
        if (quitButton.x - 35) <= mouse[0] <= (quitButton.x + quitButton.width) and quitButton.y <= mouse[1] <= (quitButton.y + quitButton.height):  
            pygame.draw.rect(screen, LIGHTCOLOR, [(quitButton.x - (35)), quitButton.y, quitButton.width, quitButton.height])
        else:
            pygame.draw.rect(screen, DARKCOLOR, [(quitButton.x - (35)), quitButton.y, quitButton.width, quitButton.height])

        if (rulesButton.x - 35) <= mouse[0] <= (rulesButton.x + quitButton.width) and rulesButton.y <= mouse[1] <= (rulesButton.y + rulesButton.height):  
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
        #same button code
        for ev in pygame.event.get():                             
            if ev.type == pygame.MOUSEBUTTONDOWN: 
                if quit2Button.x <= mouse[0] <= (quit2Button.x + quit2Button.width) and quit2Button.y <= mouse[1] <= (quit2Button.y + quit2Button.height):  
                    gameState = START
        if (quit2Button.x - 35) <= mouse[0] <= (quit2Button.x + quit2Button.width) and quit2Button.y <= mouse[1] <= (quit2Button.y + quit2Button.height):  
            pygame.draw.rect(screen, LIGHTCOLOR, [(quit2Button.x - (35)), quit2Button.y, quit2Button.width, quit2Button.height])
        else:
            pygame.draw.rect(screen, DARKCOLOR, [(quit2Button.x - (35)), quit2Button.y, quit2Button.width, quit2Button.height])
        screen.blit(textBack, (quit2Button.x, quit2Button.y))


    #INGAME is during the actual game 
    elif gameState == INGAME:                                 
        spriteBlit()
        randomBlit(meteors, phones)
        # input event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # when it is downEvent, the invaders move down the screen
            elif event.type == downEvent:                           
                handleDownEvent(invaders)
            # when it is bulletEvent, the bullets move up at a constant speed
            elif event.type == bulletEvent:                         
                handleBulletEvent(bullets, invaders)
            # during meteorEvent, if meteor.active is True, meaning that
            elif event.type == meteorEvent:                                 
                handleMeteorEvent(meteors, invaders)
            #if friend is on screen after the defender touches
            elif event.type == friendEvent:                                  
                handleFriendEvent(friends, invaders)                                                       

            #code from https://opensource.com/article/17/12/game-python-moving-player and edited
            elif event.type == pygame.KEYDOWN:
                # if the left key is moved, the defender moves left but is limited to staying on screen
                if event.key == pygame.K_LEFT:                             
                    handleLeftKey(defender, meteors, phones, friends)
                # if the right key is moved, the defender moves right but is limited to staying on screen
                elif event.key == pygame.K_RIGHT:                           
                    handleRightKey(defender, meteors, phones, friends)
                # if the space key is pressed, a bullet is spawned at the defender's location
                elif event.key == pygame.K_SPACE:                           
                    bullets.append(Bullet(defender.x, defender.y)) 


    # game over screen shown, waits for a while, then game quits
    elif gameState == LOSE:
        screen.blit(gameoverSize, (0, 0))
        if endcounter < 25:
            endcounter+=1
        else:
            pygame.quit()
    
    # win screen shown, waits for a while, then game quits
    elif gameState == WIN:
        screen.blit(youwinSize, (0, 0))
        if endcounter < 25:
            endcounter+=1
        else:
            pygame.quit()

    pygame.display.update() 





            





