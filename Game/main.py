from random import randint
import pygame
import os
import time
import Buttons
import screens

os.chdir(os.path.dirname(os.path.abspath(__file__)))
global playerHeight
global playerWidth



global sWidth
global sHeight



sWidth = 1920
sHeight = 1080

playerHeight = sHeight / 10.8
playerWidth = sWidth / 9.6

#sWidth = 1280
#sHeight = 720

global riversize

riversize = 0.5 * sWidth

global rockWidth 
global bigRockHeight 
global smallRockHeight 

rockWidth = 0.1 * sWidth
bigRockHeight = 200
smallRockHeight = 100

pygame.init()

global clock
global plankImg
plankImg = pygame.image.load('Assets/graphics/wood.png')

screen = pygame.display.set_mode((sWidth, sHeight))
pygame.display.set_caption("Raft Game")
clock = pygame.time.Clock()

sky_surface = pygame.image.load('Assets/graphics/Sky.png').convert()
sky_surface = pygame.transform.scale(sky_surface,(sWidth, sHeight))

smallRocks = []
smallRocks.append(pygame.image.load('Assets/graphics/Rocks/smallRock0.png').convert_alpha())
smallRocks.append(pygame.image.load('Assets/graphics/Rocks/smallRockT1.png').convert_alpha())
smallRocks.append(pygame.image.load('Assets/graphics/Rocks/smallRockT2.png').convert_alpha())
smallRocks.append(pygame.image.load('Assets/graphics/Rocks/smallRockT3.png').convert_alpha())
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

raftSprites = []
raftSprites.append(pygame.image.load('Assets/graphics/RaftSprites/raft2.png').convert_alpha())
raftSprites.append(pygame.image.load('Assets/graphics/RaftSprites/raft1.png').convert_alpha())
raftSprites.append(pygame.image.load('Assets/graphics/RaftSprites/raft0.png').convert_alpha())
for i in range(len(raftSprites)):raftSprites[i] = pygame.transform.scale(raftSprites[i], (playerWidth, playerHeight))


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
        
class Plank(MovingObject):

    def __init__(self):
        self.img = plankImg
        self.img = pygame.transform.scale(self.img, (rockWidth,smallRockHeight))
        self.rect = self.img.get_rect()
        super().__init__(self.rect)

        self.referenceImg = self.img  # keep the original, unscaled image around to prevent quality loss (im a retard)


class Player():

    def __init__(self):
        self.xPos = sWidth / 2
        self.maxHp = 3
        self.hp = self.maxHp
        self.width = playerWidth
        self.height = playerHeight
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

        if self.xPos > sWidth / 2 + riversize / 2 - self.width / 2: self.xPos = sWidth / 2 + riversize / 2 -self.width / 2
        if self.xPos < sWidth / 2 - riversize / 2 + self.width / 2: self.xPos = sWidth / 2 - riversize / 2 +self.width / 2


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
            self.hp -= 1
            self.spriteNum = int(self.hp / self.maxHp * (len(raftSprites) - 1))
            self.img = raftSprites[self.spriteNum]
            return True


def save_score(username, score):
    file_path = "scores.txt"
    scores = {}
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                name, old_score = line.split("-", 1)
                scores[name] = int(old_score)
    except FileNotFoundError:
        pass
    if username not in scores or score > scores[username]:
        scores[username] = score
    with open(file_path, "w", encoding="utf-8") as file:
        for name, player_score in scores.items():
            file.write(f"{name}-{player_score}\n")

    print(f"Score saved: {username} - {score}")



class RunningGame():

    def __init__(self, name):

        self.damageImg = pygame.image.load('Assets/graphics/Screens/damage.png')
        self.damageImg = pygame.transform.scale(self.damageImg, (sWidth, sHeight))
        self.healImg = pygame.image.load('Assets/graphics/Screens/heal.png')
        self.healImg = pygame.transform.scale(self.healImg, (sWidth, sHeight))
        self.healAlpha = 255
        self.damageAlpha = 0
        self.backgroungImg = sky_surface
        self.name = name
        self.score = 0
        self.lastScoreTime = time.time()
        self.font = pygame.font.Font(None, 50)
        self.river = []
        tilesize = 20
        for i in range(100, 1000, tilesize): 
            self.river.append(RoadTile(i, tilesize))
        
        self.raft = Player()
        self.joystickX = 0
        self.speed = 1
        self.countdownS = 300
        self.countdownR = 0
        self.countdownW = 0
        self.countdownH = 1000
        self.obstacles = []
        self.border = []

    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
   
        self.getInput(usesJoystick)
        self.countdownS -= 1
        self.countdownR -= self.speed
        self.countdownW -= self.speed
        self.countdownH -= self.speed

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
            self.countdownS = 300

        if self.countdownR <= 0:
            for i in range(2): self.obstacles.append(Rock(smallRocks[randint(0,3)] ))
            self.countdownR = 200

        if self.countdownW <= 0:
            self.border.append(Wall(walls[randint(0,3)],  False))
            self.border.append(Wall(walls[randint(0,3)],  True))

            self.countdownW = 25
        
        if self.countdownH <= 0:

            self.obstacles.append(Plank())
            self.countdownH = randint(1000, 2000)

    def update(self):

        self.backgroungImg = sky_surface
        if self.damageAlpha > 0:
            self.damageAlpha -= 10
        
        self.damageImg.set_alpha(self.damageAlpha)

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

        for i in range(len(self.obstacles)):
            if self.obstacles[i].detectCol(self.raft):
                if self.obstacles[i].__class__ == Plank:
                    if self.raft.heal(self.obstacles[i].xPos):
                        self.healAlpha = 255
                
                if self.raft.damage(self.obstacles[i].xPos):
                    self.damageAlpha = 255
                
    def render(self):

        screen.blit(self.backgroungImg, (0, 0)) 
        screen.blit(self.damageImg,(0,0))

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
        save_score(self.name, self.score)
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

 
if  __name__ == "__main__":
    instruction = [0]

    while True:
        match instruction[0]:
            case "start":
                p = RunningGame(instruction[1])
                p.run()
                p.raft.hitbox.centery = sHeight+500
                p.render()
                pygame.image.save(screen, 'Assets/graphics/Screens/background.png')
                instruction = ["death", instruction[1]]
            
            case "death":
                instruction = screens.deathScreen(sWidth, sHeight, p.raft, instruction[1], screen)

            case "leaderboard":
                instruction = screens.leaderboardScreen(sWidth, sHeight, screen)

            case "startscreen":
                instruction = screens.startScreen(sWidth, sHeight, screen) 

            case _ :            #default
                instruction = screens.startScreen(sWidth, sHeight, screen)