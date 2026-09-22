# Put game code here

from random import randint
import pygame
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Raft1")
clock = pygame.time.Clock()

sky_surface = pygame.image.load('Assets/graphics/Sky.png').convert()
sky_surface = pygame.transform.scale(sky_surface,(800,400))

smallRocks = []
smallRocks.append(pygame.image.load('Assets/graphics/Rocks/smallRock0.png').convert_alpha())
smallRocks.append(pygame.image.load('Assets/graphics/Rocks/smallRock1.png').convert_alpha())
smallRocks.append(pygame.image.load('Assets/graphics/Rocks/smallRock2.png').convert_alpha())
smallRocks.append(pygame.image.load('Assets/graphics/Rocks/smallRock3.png').convert_alpha())
for rock in smallRocks: rock = pygame.transform.scale(rock,(100,100))

bigRocks = []
bigRocks.append(pygame.image.load('Assets/graphics/Rocks/bigRock0.png').convert_alpha())
bigRocks.append(pygame.image.load('Assets/graphics/Rocks/bigRock1.png').convert_alpha())
bigRocks.append(pygame.image.load('Assets/graphics/Rocks/bigRock2.png').convert_alpha())
bigRocks.append(pygame.image.load('Assets/graphics/Rocks/bigRock3.png').convert_alpha())
for rock in bigRocks: rock = pygame.transform.scale(rock,(100,200))

wall = []
wall.append(pygame.image.load('Assets/graphics/Rocks/wall0.png').convert_alpha())
wall.append(pygame.image.load('Assets/graphics/Rocks/wall1.png').convert_alpha())
wall.append(pygame.image.load('Assets/graphics/Rocks/wall2.png').convert_alpha())
wall.append(pygame.image.load('Assets/graphics/Rocks/wall3.png').convert_alpha())
for rock in wall: rock = pygame.transform.scale(rock,(100,200))



class road():

    def __init__(self):
        self.orgin = (400,0)
        self.size = 1000
        self.middle = self.size/2
        self.leftcorner = (400-(self.size/2),400)
        self.rightcorner = (400+(self.size/2),400)

    def pos(self,x):
        self.middle = self.size/2-x
        self.leftcorner = (400-(self.size/2)-x,400)
        self.rightcorner = (400+(self.size/2)-x,400)
        return [self.leftcorner,self.rightcorner,self.orgin]

    def giveX(self, y):
        temp = ((self.leftcorner[0]+self.rightcorner[0])/2-400)/400 #offset dependent on y coordinate, middle of river divided by length
        return y * temp


class movingObject():

    def __init__(self,riverSize, width):
        self.zPos = 1000
        self.width = width
        self.riverSize = riverSize
        self.xPos = randint(int(self.width/2), int(self.riverSize-(self.width/2)))
        self.yPos = 0

    def updatePos(self,river,speed): #top-middle
        self.zPos -= speed
        self.yPos = 400-self.z*400/1000
        self.xPos = river.giveX(self.yPos)
    

    def detectCol(self,obj):
        if obj.xPos < self.xpos + self.width/2 and obj.xPos > self.xpos:
            return True
        return False

class Rock(movingObject):

    def __init__(self,riversize,img):
        self.width = 100
        self.img = img
        self.z = 1000
        self.height = 100
        self.mod = self.width/self.z
        self.hitbox = self.img.get_rect()
        self.hitbox.scale_by_ip(int(self.mod/self.width))
        super().__init__(riversize, self.width)

    def updatePos(self,river,speed):
        super().updatePos(river,speed)#topmiddle
        self.yPos += self.height


class player():

    def __init__(self):
        self.x = 0
        self.health = 3
        self.surface = pygame.image.load('Assets/graphics/raft.png').convert_alpha()
        self.surface = pygame.transform.scale(self.surface,(100,50))

    def update(self,x):
        x-=400
        self.x += x/50
        return self.x


river = road()
raft = player()
mouseX = 0
speed = 10
countdownS = 1000
countdownR = 0
rocks = []

while True:

    countdownS -=1
    countdownR -=1

    #if countdownS == 0:
    #    speed += 1
    #    countdownS = 100

    if countdownR <= 0:
        rocks.append(Rock(river.size,smallRocks[randint(0,3)]))
        countdownR = 100

    

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
        rock.updatePos(river,speed)
        screen.blit(rock.img,rock.hitbox)
    if rocks[0].zPos <= 0: rocks.pop(0)

    screen.blit(raft.surface,(350,350))
    pygame.display.update()
    clock.tick(60)
