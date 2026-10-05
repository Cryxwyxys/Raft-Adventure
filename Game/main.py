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

riversize = 0.5 * sWidth

global rockWidth 
global bigRockHeight 
global smallRockHeight 

rockWidth = 0.1 * sWidth
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


class RoadTile():

    def __init__(self, z, size):
        self.size = riversize
        self.zTop = z
        self.zBottom = z -size
        self.right = sWidth / 2 + riversize / 2 
        self.left = sWidth / 2 - riversize / 2
        self.yTop = self._getY_(self.zTop)
        self.yBottom = self._getY_(self.zBottom)
        
        self.points = [[self._getX_(sWidth / 2 , self.left, self.zTop), self.yTop],
                       [self._getX_(sWidth / 2 , self.right , self.zTop), self.yTop],
                       [self._getX_(sWidth / 2, self.right, self.zBottom) , self.yBottom ],
                       [self._getX_(sWidth / 2, self.left, self.zBottom), self.yBottom]]

    def update(self, xPlayer, speed):
        #self.zBottom -= speed
        #self.zTop -=speed
        self.yTop = self._getY_(self.zTop)
        self.yBottom = self._getY_(self.zBottom)
        
        self.points = [[self._getX_(xPlayer, self.left, self.zTop), self.yTop],
                       [self._getX_(xPlayer , self.right , self.zTop), self.yTop],
                       [self._getX_(xPlayer, self.right, self.zBottom) , self.yBottom ],
                       [self._getX_(xPlayer, self.left, self.zBottom), self.yBottom]]

    def _getY_(self, z):
        height = z * 3 #lowest to highest point that can be seen by Player
        y = height / 2 - 200 # how much the Player is above water level
        mod = sHeight / height #pixel pro höhe
        newY =  mod * (height - y)

        return newY

    def _getX_(self, xPlayer, xPos, z):
        width = z * 2 #left to right point that can be seen by Player
        x = width / 2 + xPlayer - xPos
        mod = sWidth / width #pixel pro höhe

        newX =  mod * (width - x)

        return newX

class MovingObject():

    def __init__(self, rect):
        self.zPos = 1000
        self.rect = rect
        self.xPos = randint(int((sWidth - riversize + rect.width) / 2), int((sWidth + riversize - rect.width ) / 2))
        self.xRenderPos = 0
        self.yRenderPos = 0
        self.OgWidth = rect.width
        self.OgHeight = rect.height
        self.hitbox = pygame.Rect(self.xPos - rect.width / 2, 0, rect.width, rect.height)

    def update(self, speed, xPlayer):
        self.move(speed)
        self.hitbox = self.newHitbox(xPlayer)
        self.img = pygame.transform.scale(self.referenceImg, (self.hitbox.width, self.hitbox.height))

    def move(self, speed):
        self.zPos -= speed

    def detectCol(self, obj):
        if self.hitbox.colliderect(obj.hitbox):

            return True

        return False
    
    def rezise(self): 
        newWidth = self.OgWidth / self.zPos / 4  * sWidth
        return newWidth

    def _getY_(self):
        height = self.zPos * 3 #lowest to highest point that can be seen by Player
        y = height / 2 - 200 # how much the Player is above water level
        mod = sHeight / height #pixel pro höhe
        newY =  mod * (height - y)

        return newY

    def _getX_(self, xPlayer):
        width = self.zPos * 2 #left to right point that can be seen by Player
        x = width / 2 + xPlayer - self.xPos # how much the Player and the rock are offset from the center
        mod = sWidth / width #pixel pro höhe

        newX =  mod * (width - x)

        return newX

    def newHitbox(self, xPlayer):   #returns a new rectangle
        newWidth = self.rezise()
        newX = self._getX_(xPlayer)
        newY = self._getY_()
        return pygame.Rect(newX - newWidth / 2, newY - self.OgHeight * newWidth / self.OgWidth / 2, newWidth, self.OgHeight * newWidth / self.OgWidth)

    def __del__(self):
        pass
        


class Rock(MovingObject):

    def __init__(self, img):

        self.rect = img.get_rect()
        super().__init__(self.rect)

        self.referenceImg = img  # keep the original, unscaled image around to prevent quality loss (im a retard)
        self.img = img
        self.height = img.get_height()

    def update(self, speed, xPlayer):
        super().update(speed, xPlayer)  


    def __del__(self):
        super().__del__()

class Wall(Rock):

    def __init__(self, img, right):
        super().__init__(img)
        self.zPos = 1200
 
        if right: 
            self.xPos = sWidth/2 + riversize / 2 + self.rect.width / 2
            pass
        else:
            self.xPos = sWidth/2 - riversize / 2 - self.rect.width / 2
            self.img = pygame.transform.flip(img, True, False)
            self.referenceImg = self.img
            pass


    def update(self, speed, xPlayer):
        super().update(speed, xPlayer)
        


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

        if self.xPos > sWidth / 2 + riversize / 2 - self.width / 2: self.xPos = sWidth / 2 + riversize / 2 -self.width / 2
        if self.xPos < sWidth / 2 - riversize / 2 + self.width / 2: self.xPos = sWidth / 2 - riversize / 2 +self.width / 2

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

        self.river = []
        tilesize = 20
        for i in range(100, 1000, tilesize): 
            self.river.append(RoadTile(i, tilesize))
        
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
            

    def spawnStuff(self):
        if self.countdownS == 0:
            self.speed += 1
            self.countdownS = 100

        if self.countdownR <= 0:
            for i in range(2): self.obstacles.append(Rock(smallRocks[randint(0,3)] ))
            self.countdownR = 200

        if self.countdownW <= 0:
            self.obstacles.append(Wall(walls[randint(0,3)],  False))
            self.obstacles.append(Wall(walls[randint(0,3)],  True))

            self.countdownW = 25

    def update(self):
            for r in self.river:
                r.update(self.raft.xPos, self.speed)

            for i in range(len(self.obstacles)):
                self.obstacles[i].update(self.speed, self.raft.xPos)
            self.raft.update(self.inputX)

            self.obstacles = [o for o in self.obstacles if o.zPos >= 150 and o.hitbox.centery < sHeight]

    def doCol(self):

        for i in range(len(self.obstacles)):
            if self.obstacles[i].detectCol(self.raft):
                self.raft.damage(self.obstacles[i].xPos)

    def render(self):

        screen.blit(sky_surface, (0, 0)) 
        for r in self.river:
            pygame.draw.polygon(screen,'BLUE', r.points, 0)
        
        for i in range(len(self.obstacles) - 1, -1 , -1):
            r = self.obstacles[i]

            screen.blit(r.img, r.hitbox) 

    
        screen.blit(self.raft.surface, (sWidth / 2 , sHeight - self.raft.height))
        pygame.display.update()

    def run(self):

        self.running = True
        while True:

            self.doATick()
            clock.tick(60)

    def doATick(self):

        self.events()
        self.spawnStuff()
        self.update()
        self.doCol()
        self.render()


if  __name__ == "__main__":
    p = RunningGame()
    p.run()



