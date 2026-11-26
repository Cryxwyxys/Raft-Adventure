import pygame
import json

import Buttons#
clock = pygame.time.Clock()

def startScreen(sWidth, sHeight, screen):

    font = pygame.font.Font(None, 60)
    gameTitleFont = pygame.font.Font(None, 100)

    startButton = Buttons.StartButton( sWidth / 2, sHeight / 4, sWidth / 16 * 2, sHeight / 9 * 2, screen)
    leaderboardButton = Buttons.LeaderboardButton(sWidth / 2, sHeight / 4 * 3, sWidth / 5, sHeight / 8, screen)
    nameField = Buttons.TextField(sWidth / 2, sHeight / 2, sWidth / 5, sHeight / 8, screen)
    exitButton = Buttons.ExitButton(sWidth / 12*11, sHeight /12, sWidth / 16, sHeight / 9, screen)
    settingsButton = Buttons.SettingsButton(sWidth / 12 , sHeight / 10, sWidth / 6, sHeight / 5, screen)

    img = pygame.image.load('Assets/graphics/Screens/Title.jpg').convert()
    img = pygame.transform.scale(img, (sWidth, sHeight))

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            nameField.handleEvent(event)

        gameTitle = gameTitleFont.render("Raft Adventure", True, "BLACK")
        titleRect = gameTitle.get_rect(center=(sWidth / 2, 100))
        
        screen.blit(img, (0, 0))
        screen.blit(gameTitle, titleRect)
        
        settingsButton.render()
        nameField.render()
        startButton.render()
        leaderboardButton.render()
        exitButton.render()

        pygame.display.update()

        if startButton.isClicked() and nameField.text != "":
            return ["start", nameField.text]

        if leaderboardButton.isClicked():
            return ["leaderboard"]
        
        if exitButton.isClicked():
            pygame.quit()
            exit()

        if settingsButton.isClicked():
            return ["settings"]

        
def deathScreen(sWidth, sHeight, raft, name, screen):
    background = pygame.image.load('Assets/graphics/Screens/background.png')

    img = pygame.image.load('Assets/graphics/Screens/death.png')
    img = pygame.transform.scale(img, (sWidth, sHeight))

    raft.hitbox.centery -= 600

    for i in range(10):
        screen.blit(background, (0,0))
        raft.hitbox.centery += sHeight / 500
        img.set_alpha(i * 30)
        screen.blit(img, (0, 0))
        screen.blit(raft.img, raft.hitbox)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        clock.tick(60)
    
    restartButton = Buttons.RestartButton(sWidth / 4, sHeight / 3 * 2, sWidth  / 6, sHeight / 5, screen)
    menuButton    = Buttons.MenuButton(sWidth / 4 * 3, sHeight / 3 * 2, sWidth / 6, sHeight / 5, screen)

    while True:
        screen.blit(img, (0,0))
        restartButton.render()
        menuButton.render()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        if restartButton.isClicked():
            return ["start",name]

        if menuButton.isClicked():
            return ["startscreen"]

def load_scores():

    scores = []

    with open("scores.json", "r", encoding="utf-8") as f:
        scores = json.load(f)

    return scores


def leaderboardScreen(sWidth, sHeight, screen):

    with open("settings.json", "r", encoding="utf-8") as f:
        settingsDict = json.load(f)
        difficulties = settingsDict["difficultiNames"]

    scores = load_scores()
    fields = []

    gameTitleFont = pygame.font.Font(None, 100)

    for i in range(len(difficulties) - 1):
        try:
            fields.append((ScoresField(sWidth / (len(difficulties)) * (i + 1) , sHeight / 5, 
                                        sWidth / (len(difficulties)  + 2), sHeight / 5 * 4,
                                        "RED", difficulties[i + 1], scores[difficulties[i + 1]], screen)))
        except KeyError: 
            pass

    menuButton = Buttons.MenuButton(sWidth /8*7, sHeight/4*3, 200, 200, screen)
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if menuButton.isClicked(): return ["startscreen"]

        screen.fill("SKYBLUE")

        title = gameTitleFont.render("LEADERBOARD", True, "WHITE")
        titleRect = title.get_rect(center=(sWidth / 2, 100))
        screen.blit(title, titleRect)

        for f in fields: 
            f.render()
        menuButton.render()

        pygame.display.update()

        clock.tick(60)

class ScoresField():
    def __init__(self, xPos, yPos, width, height, color, title, scores : dict, screen):
        self.title = title
        self.rect = pygame.Rect(xPos - width / 2, yPos , width, height)
        self.color = color
        self.scores = []
        self.screen = screen
        
        for s in scores:
            t = []
            #t.append(i + 1)
            t.append(s)
            t.append(scores[s])
            self.scores.append(t)

        self.scores.sort(key=lambda x: x[1], reverse=True)

    def render(self):

        scoreFont = pygame.font.Font(None, 45)
        nameFont = pygame.font.Font(None, 100)

        pygame.draw.rect(self.screen, self.color, self.rect)

        self.titleText = nameFont.render(self.title, True, "WHITE")
        self.titleTRect = self.titleText.get_rect()
        self.titleTRect.center = (self.rect.centerx, self.titleTRect.height * 3 / 2 + self.rect.top)
        self.screen.blit(self.titleText, self.titleTRect)
        for i in range(len(self.scores)):
            text = scoreFont.render(f"{i + 1}  {self.scores[i][0]} {self.scores[i][1]} ", True, "WHITE")
            tRect = text.get_rect()
            tRect.center = (self.rect.centerx, self.titleTRect.bottom + tRect.height * (1.5 * i + 1))
            self.screen.blit(text, tRect)

def settingsScreen(sWidth, sHeight, screen):

    with open("settings.json", "r", encoding="utf-8",) as f:
        settingsDict = json.load(f)

    font = pygame.font.Font(None, 60)
    
    tFullscreen = font.render(f"fullscreen: {settingsDict["fullscreen"]}", True, "WHITE")
    tFullscreenRect = tFullscreen.get_rect(center= (sWidth / 2, sHeight / 5))
    fullscreenButton = Buttons.OnOffButton(tFullscreenRect.right + sWidth / 10, sHeight / 5, sWidth / 10, sHeight / 10,
                                             settingsDict["fullscreen"], screen)

    difficultySlider = Buttons.Slider(sHeight / 11 * 5, sWidth / 5 * 2, sWidth / 5 * 3, sHeight / 20, 4, settingsDict["difficulty"], screen)

    n = settingsDict["difficultiNames"][settingsDict["difficulty"]]
      
    tDifficulty = font.render(f"Difficulty : {n}", True, "WHITE")
    tDifficultyRect = tDifficulty.get_rect(center= (sWidth / 2, sHeight / 7 * 3))

    tJoystick = font.render(f"Joystick connectet: {settingsDict["usesJoystick"]}", True, "WHITE")
    tJoystickRect = tJoystick.get_rect(center=(sWidth / 2, sHeight / 4 * 3))

    exitButton = Buttons.ExitButton(sWidth / 7, sHeight / 5 * 4, sWidth / 8, sHeight / 5, screen)

    controlerButton = Buttons.OnOffButton(sWidth / 4 * 3, sHeight / 4 * 3, sWidth / 10, sHeight / 10, settingsDict["usesJoystick"], screen)

    while True:
        if fullscreenButton.isClicked():
            if not t1:
                fullscreenButton.flip()
            t1 = True
            if fullscreenButton.state: settingsDict["fullscreen"] = True
            else: settingsDict["fullscreen"] = False
        else: t1 = False

        if controlerButton.isClicked():
            if not t2:
                controlerButton.flip()
            t2 = True
            if controlerButton.state: 
                if(pygame.joystick.get_count()):
                    pygame.joystick.init()
                    joystick = pygame.joystick.Joystick(0)
                    joystick.init()
                    settingsDict["usesJoystick"] = True
                else:
                    settingsDict["usesJoystick"] = False
                    controlerButton.state = False
            else: settingsDict["usesJoystick"] = False
        else: t2 = False

        if difficultySlider.isClicked() or difficultySlider.locked == False:
            difficultySlider.slide()
            settingsDict["difficulty"] = difficultySlider.getVal()

        if exitButton.isClicked():
            with open("settings.json", "w", encoding="utf-8") as f:
                
                t = json.dumps(settingsDict)
                f.write(t)
            return["startscreen",True]

        n = settingsDict["difficultiNames"][settingsDict["difficulty"]]
        tFullscreen = font.render(f"fullscreen: {settingsDict["fullscreen"]}", True, "WHITE")
        tDifficulty = font.render(f"Difficulty : {n}", True, "WHITE")
    

        screen.fill("GREY")

        screen.blit(tFullscreen, tFullscreenRect)
        screen.blit(tDifficulty, tDifficultyRect)
        screen.blit(tJoystick, tJoystickRect)
        fullscreenButton.render()
        difficultySlider.render()
        controlerButton.render()
        exitButton.render()
        
        pygame.display.update()

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
    return [0,True]