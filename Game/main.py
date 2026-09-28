from random import randint
import pygame
import os
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))



global sWidth
global sHeight
sWidth = 1920
sHeight = 1080

global riversize

riversize = 0.8 * sWidth

global rockWidth 
global bigRockHeight 
global smallRockHeight 

rockWidth = 0.2 * sWidth
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

walls = []
walls.append(pygame.image.load('Assets/graphics/Rocks/wall8.png').convert_alpha())
walls.append(pygame.image.load('Assets/graphics/Rocks/wall5.png').convert_alpha())
walls.append(pygame.image.load('Assets/graphics/Rocks/wall2.png').convert_alpha())
walls.append(pygame.image.load('Assets/graphics/Rocks/wall3.png').convert_alpha())
for i in range(len(walls)): walls[i] = pygame.transform.scale(walls[i], (200, 400))
 



if(pygame.joystick.get_count()):
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    usesJoystick = True   
else:
    usesJoystick = False



class Road():

    def __init__(self):
        self.size = riversize
        self.lenght = sHeight
        self.rect = pygame.Rect(sWidth / 2 - self.size / 2, 0 , self.size, 50)
        self.points = []

    def render(self,x):
        pass


class MovingObject():

    def __init__(self, river, width):
        self.zPos = 1000
        self.xPos = randint(int((sWidth - river.size + width) / 2), int((sWidth + river.size - width ) / 2))
        self.xRenderPos = 0
        self.yRenderPos = 0
        self.width = width
        self.hitbox = pygame.Rect(self.xPos - width / 2, 0, width, 50)

    def update(self, speed):
        self.move(speed)

    def move(self, speed):
        self.zPos -= speed
        self.hitbox.bottom += speed

    def detectCol(self, obj):
        if self.hitbox.colliderect(obj.hitbox):
            print("col")
            return True

        return False


class Rock(MovingObject):

    def __init__(self, img, river):

        self.width = img.get_width()
        super().__init__(river, self.width)

        self.referenceImg = img  # keep the original, unscaled image around to prevent quality loss (im a retard)
        self.img = img
        self.height = img.get_height()

    def update(self, speed):
        super().update(speed)  

        def __del__(self):
            pass


class Wall(Rock):

    def __init__(self, img, river, right):
        super().__init__(img, river)
        if right: 
            self.xPos = sWidth/2 + riversize / 2 + self.width / 2
        else:
            self.xPos = sWidth/2 - riversize / 2 - self.width / 2
            self.img = pygame.transform.flip(img, True, False)
            self.referenceImg = self.img

        self.hitbox.x = self.xPos - self.width / 2

    def update(self, speed):
        super().update(speed)


class Player():

    def __init__(self):
        self.lives = 3
        self.xPos = sWidth / 2
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

    def update(self, x):

        #if(time.time()-self.lasthit > 2):
        self.updatePos(x)
        self.updateVis()
        return self.xPos

    def updatePos(self, x):
        self.xPos += (int(x) / 50)

        if self.xPos > sWidth / 2 + riversize / 2 : self.xPos = sWidth / 2 + riversize / 2
        if self.xPos < sWidth / 2 - riversize / 2 : self.xPos = sWidth / 2 - riversize / 2

        self.hitbox.update(self.xPos - self.width / 2, self.hitbox.top, self.width, self.height) 

    def updateVis(self):

        if time.time() - self.lasthit > 1:
            self.surface = self.img

        pygame.draw.rect(screen, 'RED', self.hitbox, 10, 10)



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
        self.obstacles = []

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
            self.obstacles.append(Rock(smallRocks[randint(0,3)], self.river))
            self.countdownR = 90

        if self.countdownW <= 0:
            self.obstacles.append(Wall(walls[randint(0,3)], self.river, False))
            self.obstacles.append(Wall(walls[randint(0,3)], self.river, True))

            self.countdownW = 20

    def update(self):

            for i in range(len(self.obstacles)):
                self.obstacles[i].update(self.speed)
            self.raft.update(self.inputX)

            temp = len(self.obstacles)

            for i in range(temp):
                if self.obstacles[i].hitbox.top > sHeight:
                    self.obstacles.pop(i)
                    i -= 1
                    temp -= 1
                else: break

    def doCol(self):

        for i in range(len(self.obstacles)):
            if self.obstacles[i].detectCol(self.raft):
                self.raft.damage(self.obstacles[i].xPos)
            else: break

    def render(self):

        screen.blit(sky_surface, (0, 0)) 

        for rock in self.obstacles:
            screen.blit(rock.img, rock.hitbox)
        
        screen.blit(self.raft.surface, self.raft.hitbox)

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