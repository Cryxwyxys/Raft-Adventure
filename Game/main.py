from random import randint
import pygame
import os
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

global riversize

riversize = 1000

global sWidth
global sHeight
sWidth = 800
sHeight = 600

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
 



if(pygame.joystick.get_count()):
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    usesJoystick = True   
else:
    usesJoystick = False



class Road():

    def __init__(self):
        self.orgin = (sWidth/2, 0)
        self.size = riversize
        self.leftcorner = (sWidth/2 - (self.size/2), sHeight)
        self.rightcorner = (sWidth/2 + (self.size/2), sHeight)
        self.offsetFactor = (self.leftcorner[0]+self.rightcorner[0] - sWidth) / 2  / sHeight

    def pos(self,x):
        self.leftcorner = (sWidth/2 - (self.size/2) - x, sHeight)
        self.rightcorner = (sWidth/2 + (self.size/2) - x, sHeight)
        self.offsetFactor = (self.leftcorner[0]+self.rightcorner[0] - sWidth) / 2  / sHeight
        return [self.leftcorner,self.rightcorner,self.orgin]


class MovingObject():

    def __init__(self, width):
        self.zPos = 1000
        self.riverSize = riversize
        self.offset = randint(int(sWidth/2-riversize/2 + width/2), int(sWidth/2 + riversize/2 - width/2))
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
        if self.hitbox.colliderect(obj.hitbox):
            return True
        return False


class Rock(MovingObject):

    def __init__(self, img):
        self.width = img.get_width()
        self.orig_img = img  # keep the original, unscaled image around to prevent quality loss (im a retard)
        self.img = img
        self.zPos = 1000
        self.height = img.get_height()
        self.mod = (1000 - self.zPos) / 1000
        self.hitbox = self.img.get_rect()
        super().__init__( self.width)

    def update(self, river, speed):
        super().update( river, speed)  # topmiddle
        self.mod = (1000 - self.zPos) / 1000
        if self.mod < 0:
            self.mod = 0
        self.width = max(1, int(self.mod * self.orig_img.get_width()))
        self.height = max(1, int(self.mod * self.orig_img.get_height()))
        self.img = pygame.transform.scale(self.orig_img, (self.width, self.height))  # always scale from the original
        self.yPos += self.height / 2  # middle
        self.hitbox = self.img.get_rect(center=(self.xPos, self.yPos))

        def __del__(self):
            pass


class Wall(Rock):

    def __init__(self, img, right):
        super().__init__( img)
        if right: 
            self.offset = sWidth/2 + riversize / 2 + self.width / 2
        else:
            self.offset = sWidth/2 - riversize / 2 - self.width / 2
            self.img = pygame.transform.flip(img, True, False)
            self.orig_img = self.img

    def update(self, river, speed):
        super().update(river, speed)            # Rock.update: setzt Größe + self.yPos aufs Zentrum
        bottom_y = self.yPos + self.height / 2   # unteres, spielernahes Ende statt oberer Sprite-Kante
        self.xPos = self.xAt(bottom_y)
        self.hitbox.centerx = self.xPos


class Player():

    def __init__(self):
        self.lives = 3
        self.xPos = 0
        self.health = 3
        self.width = 150
        self.height = 100
        self.surface = pygame.image.load('Assets/graphics/raft.png').convert_alpha()
        self.surface = pygame.transform.scale(self.surface,(self.width, self.height))
        self.hitbox = self.surface.get_rect()
        self.hitbox.center = (sWidth/2, sHeight - self.height/2)
        self.img = self.surface

        self.invisFrames = 3
        self.lasthit = time.time()

    def update(self,x):

        if(time.time()-self.lasthit > 2):
            self.updatePos(x)
        self.updateVis()

        return self.xPos

    def updatePos(self, x):
        self.xPos += (int(x) / 50)

        if abs(self.xPos) > riversize / 2: 
            if x > 0 : self.xPos = riversize / 2
            else: self.xPos = 0 - riversize / 2


    def updateVis(self):
        if time.time() - self.lasthit > 1:
            self.surface = self.img

    def damage(self, x):

        if time.time() - self.lasthit > self.invisFrames:
            self.lives -= 1

            if self.xPos > x:
                self.xPos += 100
                self.surface = pygame.transform.rotate(self.img, 15)
            else: 
                self.xPos -= 100
                self.surface = pygame.transform.rotate(self.img, -15)

            self.lasthit = time.time()


class RunningGame():

    def __init__(self):

        self.river = Road()
        self.raft = Player()
        self.joystickX = 0
        self.speed = 1
        self.countdownS = 100000
        self.countdownR = 0
        self.countdownW = 0
        self.rocks = []

    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
   
        self.getInput(usesJoystick)
        self.countdownS -= 1
        self.countdownR -= self.speed
        self.countdownW -= self.speed

    

    def getInput(self, usesJoystick):

        if(usesJoystick):
            self.joystickX = round(joystick.get_axis(0),2) 
            self.inputX = self.joystickX * sWidth / 2

        else:
            temp =  pygame.mouse.get_pos()
            self.inputX = temp[0] - sWidth / 2
            

    def spawnRocks(self):
        if self.countdownS == 0:
            self.speed += 1
            self.countdownS = 100

        if self.countdownR <= 0:
            self.rocks.append(Rock(smallRocks[randint(0,3)]))
            self.countdownR = 90

        if self.countdownW <= 0:
            self.rocks.append(Wall(wall[randint(0,3)],0))
            self.rocks.append(Wall(wall[randint(0,3)],1))

            self.countdownW = 20

    def update(self):

            for i in range(len(self.rocks)):
                self.rocks[i].update(self.river, self.speed)
            self.raft.update(self.inputX)

            temp = len(self.rocks)
            for i in range(temp):
                if self.rocks[i].yPos - self.rocks[i].height / 2 > sHeight:
                    self.rocks.pop(i)
                    i -= 1
                    temp -= 1
                else: break

    def doCol(self):

        for i in range(len(self.rocks)):
            if self.rocks[i].yPos + self.rocks[i].height/2 >= sHeight: 
                if self.rocks[i].detectCol(self.raft):
                    self.raft.damage(self.rocks[i].xPos)
            else: break

    def render(self):

        screen.blit(sky_surface, (0, 0)) 
        pygame.draw.polygon(screen,'BLUE',self.river.pos(self.raft.xPos))

        for rock in self.rocks:
            screen.blit(rock.img, rock.hitbox)

        screen.blit(self.raft.surface,((sWidth-self.raft.width)/2,sHeight-self.raft.height))

        pygame.display.update()

    def run(self):

        self.running = True
        while True:

            self.doATick()
            clock.tick(60)

    def doATick(self):

        self.events()
        self.spawnRocks()
        self.update()
        self.doCol()
        self.render()



if  __name__ == "__main__":
    p = RunningGame()
    p.run()