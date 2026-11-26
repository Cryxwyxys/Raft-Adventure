from random import randint
import pygame
import os
import time
import json


global clock
global plankImg
global sky_surface
global smallRocks
global walls
global raftSprites


os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()
pygame.display.init()

plankImg = pygame.image.load('Assets/graphics/wood.png')

clock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0))
sky_surface = pygame.image.load('Assets/graphics/Sky.png').convert()

smallRocks = []
smallRocks.append(pygame.image.load('Assets/graphics/Rocks/smallRock0.png').convert_alpha())
smallRocks.append(pygame.image.load('Assets/graphics/Rocks/smallRockT1.png').convert_alpha())
smallRocks.append(pygame.image.load('Assets/graphics/Rocks/smallRockT2.png').convert_alpha())
smallRocks.append(pygame.image.load('Assets/graphics/Rocks/smallRockT3.png').convert_alpha())

walls = []
walls.append(pygame.image.load('Assets/graphics/Rocks/wall8.png').convert_alpha())
walls.append(pygame.image.load('Assets/graphics/Rocks/wall5.png').convert_alpha())
walls.append(pygame.image.load('Assets/graphics/Rocks/wall2.png').convert_alpha())
walls.append(pygame.image.load('Assets/graphics/Rocks/wall3.png').convert_alpha())

raftSprites = []
raftSprites.append(pygame.image.load('Assets/graphics/RaftSprites/raft2.png').convert_alpha())
raftSprites.append(pygame.image.load('Assets/graphics/RaftSprites/raft1.png').convert_alpha())
raftSprites.append(pygame.image.load('Assets/graphics/RaftSprites/raft0.png').convert_alpha())
    


class RoadTile():

    def __init__(self, z, height):
        self.zTop = z
        self.zBottom = z - height
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

    def __init__(self, img, right, pos):
        super().__init__(img)
        self.zPos = pos
 
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
        
class Plank(MovingObject):

    def __init__(self):
        self.img = plankImg
        self.img = pygame.transform.scale(self.img, (rockWidth,smallRockHeight))
        self.rect = self.img.get_rect()
        super().__init__(self.rect)

        self.referenceImg = self.img  # keep the original, unscaled image around to prevent quality loss (im a retard)


class Player():

    def __init__(self,hp):
        
        self.xPos = sWidth / 2
        self.maxHp = hp
        self.hp = self.maxHp
        self.width = sWidth /6
        self.height = sHeight / 8
        for i in range(len(raftSprites)):raftSprites[i] = pygame.transform.scale(raftSprites[i], (self.width, self.height))

        self.spriteNum = int(self.hp / self.maxHp * (len(raftSprites) - 1))
        self.surface = raftSprites[self.spriteNum]
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


    def updateVis(self):

        if time.time() - self.lasthit > 1:
            self.surface = self.img

        pygame.draw.rect(screen, 'RED', self.hitbox, 10, 10)

    def damage(self, x):

        if time.time() - self.lasthit > self.invisFrames:
            self.hp -= 1
            self.spriteNum = int(self.hp / self.maxHp * (len(raftSprites) - 1))
            self.img = raftSprites[self.spriteNum]

            if self.xPos > x:
                self.xPos += 100
                self.surface = pygame.transform.rotate(self.img, 15)
            else: 
                self.xPos -= 100
                self.surface = pygame.transform.rotate(self.img, -15)

            self.lasthit = time.time()
            return True
        return False

    def heal(self):
        if self.hp < self.maxHp:
            self.hp += 1
            self.spriteNum = int(self.hp / self.maxHp * (len(raftSprites) - 1))
            self.img = raftSprites[self.spriteNum]
            return True
        return False


def save_score(username, score, dif):
    file_path = "scores.json"
    
    with open(file_path, "r", encoding="utf-8") as f:
        allScores = json.load(f)
    try:
        scores = allScores[dif]
    except KeyError:
        allScores[dif] = {}
        scores = allScores[dif]

    if username not in scores or scores[username] < score:
        scores[username] = score
        allScores[dif] = scores

    with open(file_path, "w", encoding="utf-8") as f:
        t = json.dumps(allScores)
        f.write(t)



class RunningGame():

    def __init__(self, name, screenWidth, screenHeight, givenScreen,):

        global sWidth
        global sHeight
        global smallRockHeight 
        global rockWidth 
        global screen
        global riversize

        with open("settings.json", "r", encoding= "utf-8") as f:
            self.settingsDict = json.load(f)
        sWidth = screenWidth
        sHeight = screenHeight
        screen = givenScreen

            
        riversize = 0.5 * sWidth
        self.difficulty = self.settingsDict["difficulty"]
        
        self.usesJoystick = self.settingsDict["usesJoystick"]
        rockWidth = 0.1 * sWidth
        smallRockHeight = sHeight / 7

        for i in range(len(smallRocks)): smallRocks[i] = pygame.transform.scale(smallRocks[i], (rockWidth, smallRockHeight))
        for i in range(len(walls)): walls[i] = pygame.transform.scale(walls[i], (200, 400))

        self.river = []
        tilesize = 20
        for i in range(100, 1000, tilesize):
            self.river.append(RoadTile(i, tilesize))

        self.damageImg = pygame.image.load('Assets/graphics/Screens/damage.png')
        self.damageImg = pygame.transform.scale(self.damageImg, (sWidth, sHeight))

        self.healImg = pygame.image.load('Assets/graphics/Screens/heal.png')
        self.healImg = pygame.transform.scale(self.healImg, (sWidth, sHeight))

        self.healAlpha = 0
        self.damageAlpha = 0
        self.backgroungImg = pygame.transform.scale(sky_surface,(sWidth, sHeight))
        self.name = name
        self.score = 0
        self.lastScoreTime = time.time()
        self.font = pygame.font.Font(None, 50)
        
        self.raft = Player(self.settingsDict["lives"][self.difficulty])
        self.joystickX = 0
        self.speed = self.settingsDict["speed"][self.difficulty]
        self.countdownS = self.settingsDict["acceleration"][self.difficulty]
        self.countdownR = self.settingsDict["countdownR"][self.difficulty]
        self.countdownW = 0
        self.countdownH = self.settingsDict["countdownH"][self.difficulty]
        self.obstacles = []
        self.border = []
        for i in range(int(1200 / 25)):
            self.border.append(Wall(walls[randint(0,3)],  False, i * 25))
            self.border.append(Wall(walls[randint(0,3)],  True, i * 25))
            

    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
   
        self.getInput()
        self.countdownS -= 1
        self.countdownR -= self.speed
        self.countdownW -= self.speed
        self.countdownH -= self.speed

    def getInput(self):

        if(self.usesJoystick):
            self.joystickX = round(joystick.get_axis(0),2) 
            self.inputX = self.joystickX * sWidth / 2

        else:
            temp =  pygame.mouse.get_pos()
            self.inputX = temp[0] - sWidth / 2
            

    def spawnStuff(self):

        if self.countdownS == 0:
            self.speed += 1
            self.countdownS = self.settingsDict["acceleration"][self.difficulty]

        if self.countdownR <= 0:
            for i in range(2): self.obstacles.append(Rock(smallRocks[randint(0,3)] ))
            self.countdownR = self.settingsDict["countdownR"][self.difficulty]

        if self.countdownW <= 0:
            self.border.append(Wall(walls[randint(0,3)],  False, 1200))
            self.border.append(Wall(walls[randint(0,3)],  True, 1200))

            self.countdownW = 25
        
        if self.countdownH <= 0:

            self.obstacles.append(Plank())
            self.countdownH = self.settingsDict["countdownH"][self.difficulty]

    def update(self):

        if self.damageAlpha > 0:
            self.damageAlpha -= 10

        if self.healAlpha > 0:
            self.healAlpha -= 10

        self.damageImg.set_alpha(self.damageAlpha)
        self.healImg.set_alpha(self.healAlpha)

        for r in self.river:
            r.update(self.raft.xPos, self.speed)

        self.border = [o for o in self.border if o.zPos >= 150 and o.hitbox.centery < sHeight]
        self.obstacles = [o for o in self.obstacles if o.zPos >= 150 and o.hitbox.centery < sHeight]

        for i in range(len(self.obstacles)):
            self.obstacles[i].update(self.speed, self.raft.xPos)

        for i in range(len(self.border)):
            self.border[i].update(self.speed, self.raft.xPos)

        self.raft.update(self.inputX)


    def doCol(self):

        for i in range(len(self.obstacles) - 2):
            if self.obstacles[i].detectCol(self.raft):
                if self.obstacles[i].__class__ == Plank:
                    if self.raft.heal():
                        self.healAlpha = 255
                        self.obstacles.pop(i)
                else:
                    if self.raft.damage(self.obstacles[i].xPos):
                        self.damageAlpha = 255
                
    def render(self):

        screen.blit(self.backgroungImg, (0, 0)) 
        screen.blit(self.damageImg,(0,0))
        screen.blit(self.healImg,(0,0))


        for r in self.river:
            pygame.draw.polygon(screen,'BLUE', r.points, 0)

        for i in range(len(self.border) - 1, -1 , -1):
            r = self.border[i]
            screen.blit(r.img, r.hitbox) 

        for i in range(len(self.obstacles) - 1, -1 , -1):
            r = self.obstacles[i]
            screen.blit(r.img, r.hitbox) 

        
        screen.blit(self.raft.surface,  self.raft.hitbox)
        self.drawScore()
        pygame.display.update()

    def run(self):

        self.running = True

        while True:
            self.doATick()
            if self.raft.hp == 0:
                return

            clock.tick(60)


    def death(self):
        name = self.settingsDict["difficultiNames"][self.difficulty]
        save_score(self.name, self.score, name)
        self.damageAlpha = 0

    def doATick(self):

        self.events()
        self.spawnStuff()
        self.update()
        self.doCol()
        self.updateScore()
        self.render()

        if not self.raft.hp:
            r = self.death()

    def updateScore(self):
        currentTime = time.time()

        if currentTime - self.lastScoreTime >= 1:
            self.score += 1
            self.lastScoreTime = currentTime

    def drawScore(self):
        scoreText = self.font.render(f"Score: {self.score}", True, "WHITE")

        scoreRect = scoreText.get_rect()
        scoreRect.topleft = (50, 50)

        pygame.draw.rect(screen, "BLACK", scoreRect.inflate(30, 20))

        screen.blit(scoreText, scoreRect)
