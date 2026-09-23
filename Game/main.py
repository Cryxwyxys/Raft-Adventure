# Put game code here

from random import randint
import pygame
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

global sWidth
global sHeight
sWidth = 1600
sHeight = 800

global rockWidth 
global bigRockHeight 
global smallRockHeight 

rockWidth = 100
bigRockHeight = 200
smallRockHeight = 100

pygame.init()
screen = pygame.display.set_mode((sWidth, sHeight))
pygame.display.set_caption("Raft1")
clock = pygame.time.Clock()

sky_surface = pygame.image.load('Assets/graphics/Sky.png').convert()
sky_surface = pygame.transform.scale(sky_surface,(sWidth, sHeight))

smallRocks = []
smallRocks.append(pygame.image.load('Assets/graphics/Rocks/smallRock0.png').convert_alpha())
smallRocks.append(pygame.image.load('Assets/graphics/Rocks/smallRock1.png').convert_alpha())
smallRocks.append(pygame.image.load('Assets/graphics/Rocks/smallRock2.png').convert_alpha())
smallRocks.append(pygame.image.load('Assets/graphics/Rocks/smallRock3.png').convert_alpha())
for rock in smallRocks: rock = pygame.transform.scale(rock, (rockWidth, smallRockHeight))

bigRocks = []
bigRocks.append(pygame.image.load('Assets/graphics/Rocks/bigRock0.png').convert_alpha())
bigRocks.append(pygame.image.load('Assets/graphics/Rocks/bigRock1.png').convert_alpha())
bigRocks.append(pygame.image.load('Assets/graphics/Rocks/bigRock2.png').convert_alpha())
bigRocks.append(pygame.image.load('Assets/graphics/Rocks/bigRock3.png').convert_alpha())
for rock in bigRocks: rock = pygame.transform.scale(rock, (rockWidth, smallRockHeight))

wall = []
wall.append(pygame.image.load('Assets/graphics/Rocks/wall0.png').convert_alpha())
wall.append(pygame.image.load('Assets/graphics/Rocks/wall1.png').convert_alpha())
wall.append(pygame.image.load('Assets/graphics/Rocks/wall2.png').convert_alpha())
wall.append(pygame.image.load('Assets/graphics/Rocks/wall3.png').convert_alpha())
for rock in wall: rock = pygame.transform.scale(rock, (100, 200))



class Road():

    def __init__(self):
        self.orgin = (sWidth/2, 0)
        self.size = 1000
        self.leftcorner = (sWidth/2 - (self.size/2), sHeight)
        self.rightcorner = (sWidth/2 + (self.size/2), sHeight)

    def pos(self,x):
        self.leftcorner = (sWidth/2 - (self.size/2) - x, sHeight)
        self.rightcorner = (sWidth/2 + (self.size/2) - x, sHeight)
        self.offsetFactor = (self.leftcorner[0]+self.rightcorner[0] - sWidth) / 2  / sHeight
        return [self.leftcorner,self.rightcorner,self.orgin]


class MovingObject():

    def __init__(self,riverSize, width):
        self.zPos = 1500 #outside the window because of the screen needing time to boot I think
        self.width = width
        self.riverSize = riverSize
        self.offset = randint(int(sWidth/2-riverSize/2 + width/2), int(sWidth/2 + riverSize/2 - width/2))
        self.xPos = sWidth / 2
        self.yPos = 0

    def update(self,river,speed): #top-middle
        self.zPos -= speed / self.zPos * 1000
        self.yPos = sHeight - self.zPos * sHeight / 1000
        self.xPos = river.offsetFactor * self.yPos + sWidth / 2 
    

    def detectCol(self,obj):
        if obj.xPos < self.xpos + self.width/2 and obj.xPos > self.xpos:
            return True
        return False


class Rock(MovingObject):

    def __init__(self, riversize, img):
        self.width = rockWidth
        self.orig_img = img  # keep the original, unscaled image around
        self.img = img
        self.z = 1000
        self.height = 100
        self.mod = (1000 - self.z) / 1000
        self.hitbox = self.img.get_rect()
        self.hitbox.scale_by_ip(int(self.mod * self.width))
        super().__init__(riversize, self.width)

    def update(self, river, speed):
        super().update(river, speed)  # topmiddle
        self.mod = (1000 - self.zPos) / 1000
        if self.mod < 0:
            self.mod = 0
        self.width = max(1, int(self.mod * rockWidth))
        self.height = max(1, int(self.mod * smallRockHeight))
        self.img = pygame.transform.scale(self.orig_img, (self.width, self.height))  # always scale from the original
        self.yPos += self.height / 2  # middle
        self.hitbox = self.img.get_rect(center=(self.xPos, self.yPos))


class Wall(Rock):

    def __init__(self, riversize, img, b):
        super().__init__(self, riversize, img)
        self.height = 800
        self.width = self.img.get.width 
        if b : self.offset = sWidth/2 + riversize / 2
        else : 
            self.offset = sWidth/2 - riversize / 2
            self.img = pygame.transform.flip(self.img,0,1)

    def update(self, river , speed):
        super().update(river, speed)


class Player():

    def __init__(self):
        self.x = 0
        self.health = 3
        self.width = 100
        self.height = 50
        self.surface = pygame.image.load('Assets/graphics/raft.png').convert_alpha()
        self.surface = pygame.transform.scale(self.surface,(self.width, self.height))

    def update(self,x):
        x -= sWidth / 2
        self.x += x / 50
        return self.x


river = Road()
raft = Player()
mouseX = 0
speed = 1
countdownS = 100000
countdownR = 0
countdownW = 0
rocks = []

while True:

    countdownS -= 1
    countdownR -= speed
    countdownW -= speed

    if countdownS == 0:
        speed += 1
        countdownS = 100

    if countdownR <= 0:
        rocks.append(Rock(river.size,smallRocks[randint(0,3)]))
        countdownR = 100

    if countdownW <= 0:
        rocks.append(Rock(river.size,wall[randint(0,3)]))
        countdownR = 10

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEMOTION:
            mouseX = event.pos[0]

    x = raft.update(mouseX)

    
    screen.blit(sky_surface, (0, 0)) 
    pygame.draw.polygon(screen,'BLUE',river.pos(x))

    for rock in rocks:
        rock.update(river,speed)
        screen.blit(rock.img, rock.hitbox)
        print(f"{rock.hitbox},{rock.img}")
        
    if rocks[0].zPos <= 0: rocks.pop(0)
    screen.blit(raft.surface,((sWidth-raft.width)/2,sHeight-raft.height))
    pygame.display.update()
    clock.tick(60)