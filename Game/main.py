from random import randint
import pygame
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

global sWidth
global sHeight
sWidth = 1920
sHeight = 1080

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
for i in range(len(smallRocks)): smallRocks[i] = pygame.transform.scale(smallRocks[i], (rockWidth, smallRockHeight))

bigRocks = []
bigRocks.append(pygame.image.load('Assets/graphics/Rocks/bigRock0.png').convert_alpha())
bigRocks.append(pygame.image.load('Assets/graphics/Rocks/bigRock1.png').convert_alpha())
bigRocks.append(pygame.image.load('Assets/graphics/Rocks/bigRock2.png').convert_alpha())
bigRocks.append(pygame.image.load('Assets/graphics/Rocks/bigRock3.png').convert_alpha())
for i in range(len(bigRocks)): bigRocks[i] = pygame.transform.scale(bigRocks[i], (rockWidth, bigRockHeight))

wall = []
wall.append(pygame.image.load('Assets/graphics/Rocks/wall8.png').convert_alpha())
wall.append(pygame.image.load('Assets/graphics/Rocks/wall5.png').convert_alpha())
wall.append(pygame.image.load('Assets/graphics/Rocks/wall2.png').convert_alpha())
wall.append(pygame.image.load('Assets/graphics/Rocks/wall3.png').convert_alpha())
for i in range(len(wall)): wall[i] = pygame.transform.scale(wall[i], (200, 400))
 


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

    def __init__(self, riverSize, width):
        self.zPos = 1000
        self.riverSize = riverSize
        self.offset = randint(int(sWidth/2-riverSize/2 + width/2), int(sWidth/2 + riverSize/2 - width/2))
        self.xPos = sWidth / 2
        self.yPos = 0

    def xAt(self, y):
        # x-Position der Fluss-Kante (inkl. Lenkung und seitlichem offset) bei Tiefe y
        deviation = self.offset - sWidth / 2
        scaled = deviation * (y / sHeight)
        return self.river.offsetFactor * y + sWidth / 2 + scaled

    def update(self, river, speed):
        self.river = river
        self.zPos -= speed / self.zPos * 1000
        self.yPos = sHeight - self.zPos * sHeight / 1000
        self.xPos = self.xAt(self.yPos)

    def detectCol(self, obj):
        if obj.xPos < self.xPos + self.width/2 and obj.xPos > self.xPos:
            return True
        return False





class Rock(MovingObject):

    def __init__(self, riversize, img):
        self.width = img.get_width()
        self.orig_img = img  # keep the original, unscaled image around to prevent quality loss (im a retard)
        self.img = img
        self.zPos = 1000
        self.height = img.get_height()
        self.mod = (1000 - self.zPos) / 1000
        self.hitbox = self.img.get_rect()
        super().__init__(riversize, self.width)

    def update(self, river, speed):
        super().update(river, speed)  # topmiddle
        self.mod = (1000 - self.zPos) / 1000
        if self.mod < 0:
            self.mod = 0
        self.width = max(1, int(self.mod * self.orig_img.get_width()))
        self.height = max(1, int(self.mod * self.orig_img.get_height()))
        self.img = pygame.transform.scale(self.orig_img, (self.width, self.height))  # always scale from the original
        self.yPos += self.height / 2  # middle
        self.hitbox = self.img.get_rect(center=(self.xPos, self.yPos))

        def __del__(self):
            print(f"i was deleted at {self.yPos}")


class Wall(Rock):

    def __init__(self, riversize, img, b):
        super().__init__(riversize, img)
        if b: self.offset = sWidth/2 + riversize / 2 + self.width / 2
        else:
            self.offset = sWidth/2 - riversize / 2 - self.width / 2
            self.img = pygame.transform.flip(self.img, 1, 0)

    def update(self, river, speed):
        super().update(river, speed)            # Rock.update: setzt Größe + self.yPos aufs Zentrum
        bottom_y = self.yPos + self.height / 2   # unteres, spielernahes Ende statt oberer Sprite-Kante
        self.xPos = self.xAt(bottom_y)
        self.hitbox.centerx = self.xPos


class Player():

    def __init__(self):
        self.xPos = 0
        self.health = 3
        self.width = 100
        self.height = 50
        self.surface = pygame.image.load('Assets/graphics/raft.png').convert_alpha()
        self.surface = pygame.transform.scale(self.surface,(self.width, self.height))
        self.hitbox = self.surface.get_rect()

    def update(self,x):
        x -= sWidth / 2
        self.xPos += x / 50
        return self.xPos

    def damage(self, x):
        print("col")
        pass


river = Road()
raft = Player()
mouseX = 0
speed = 1
countdownS = 100000
countdownR = 0
countdownW = 0
rocks = []
walls = []

while True:

    countdownS -= 1
    countdownR -= speed
    countdownW -= speed

    if countdownS == 0:
        speed += 1
        countdownS = 100

    if countdownR <= 0:
        rocks.append(Rock(river.size,smallRocks[randint(0,3)]))
        countdownR = 90

    if countdownW <= 0:
        walls.append(Wall(river.size,wall[randint(0,3)],0))
        walls.append(Wall(river.size,wall[randint(0,3)],1))

        countdownW = 20

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEMOTION:
            mouseX = event.pos[0]

    x = raft.update(mouseX)

    screen.blit(sky_surface, (0, 0)) 
    pygame.draw.polygon(screen,'BLUE',river.pos(x))

    for cliff in walls:
        cliff.update(river, speed)
        screen.blit(cliff.img, cliff.hitbox)

    for i in range(len(rocks)):
        rocks[i].update(river, speed)
        screen.blit(rocks[i].img, rocks[i].hitbox)
       
    if rocks[0].yPos + rocks[0].height/2 >= sHeight: 
        if rocks[0].detectCol(raft):
            raft.damage(rocks[0].xPos)
        rocks.pop(0)

    if walls[0].yPos >= sHeight: 
        if walls[0].detectCol(raft) :
            raft.damage(walls[0].xPos)
        walls.pop(0)

    screen.blit(raft.surface,((sWidth-raft.width)/2,sHeight-raft.height))
    pygame.display.update()
    clock.tick(60)