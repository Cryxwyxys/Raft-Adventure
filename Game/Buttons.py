# buttons for menu screens

import pygame
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Button():
    
    def __init__(self, xMiddle, yMiddle, width, height, screen, normalImg, hoveringImg):
        self.xMiddle = xMiddle
        self.yMiddle = yMiddle
        self.width = width
        self.height = height
        self.imgN = pygame.image.load(normalImg).convert_alpha()
        self.imgP = pygame.image.load(hoveringImg).convert_alpha()
        self.imgN = pygame.transform.scale(self.imgN, (width, height))
        self.imgP = pygame.transform.scale(self.imgP, (width, height))
        self.rect = pygame.Rect(xMiddle - width / 2, yMiddle - height / 2, width, height)
        self.screen = screen
        
    def checkHovering(self):
        m = pygame.mouse.get_pos()
        self.hovering = self.rect.collidepoint(m)

    def isClicked(self):
        mousePos = pygame.mouse.get_pos()
        
        self.hovering = self.rect.collidepoint(mousePos)
        self.down = pygame.mouse.get_pressed()[0]
        return self.hovering and self.down

    def render(self):
        self.checkHovering()
        if self.hovering:
            self.screen.blit(self.imgP, self.rect)
        else:
            self.screen.blit(self.imgN, self.rect)
        

class StartButton(Button):

    def __init__(self, xMiddle, yMiddle, width, height, screen):
        super().__init__(xMiddle, yMiddle, width, height, screen, "Assets/graphics/Buttons/redButton.png", "Assets/graphics/Buttons/redButtonPressed.png")

    def checkHovering(self):
        super().checkHovering()

    def isClicked(self):
        val = super().isClicked()
        return val

    def render(self):
        super().render()


class RestartButton(Button):
    def __init__(self, xMiddle, yMiddle, width, height, screen):
        super().__init__(xMiddle, yMiddle, width, height, screen, "Assets/graphics/Buttons/restart.png", "Assets/graphics/Buttons/restartP.png")

    def checkHovering(self):
        super().checkHovering()

    def isClicked(self):
        val = super().isClicked()
        return val


class TextField(Button):

    def __init__(self, xMiddle, yMiddle, width, height, screen):

        self.text = ""
        self.font = pygame.font.SysFont(None, 36)
        self.active = False   #checks if textinput should go in that field
        displaytext = self.font.render(self.text, True, 'BLACK')
        textRect = displaytext.get_rect()

        super().__init__(xMiddle, yMiddle, textRect.width + 200, height, screen,
                          'Assets/graphics/Buttons/textField.png', "Assets/graphics/Buttons/textFieldP.png")

    def handleEvent(self, event): # needs to be put in the for pygame.event.get loop
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)   #checks if the field has been selectet

        elif self.active and event.type == pygame.KEYDOWN:    #checks for backspace
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]                    #removes last char from string

        elif self.active and event.type == pygame.TEXTINPUT:      
            self.text += event.text                           #adds textinput to text

    def render(self):
        if self.active or self.text != "":
            self.screen.blit(self.imgN, self.rect)
        else:
            self.screen.blit(self.imgP, self.rect)

        displaytext = self.font.render(self.text, True, 'BLACK')
        textRect = displaytext.get_rect(center=self.rect.center)
        self.screen.blit(displaytext, textRect)


class LeaderboardButton(Button):

    def __init__(self, xMiddle, yMiddle, width, height, screen):
        super().__init__(xMiddle, yMiddle, width, height, screen,
            "Assets/graphics/Buttons/leaderboard.png", "Assets/graphics/Buttons/leaderboardP.png")

class MenuButton(Button):

    def __init__(self, xMiddle, yMiddle, width, height, screen):
        super().__init__(
            xMiddle,
            yMiddle,
            width,
            height,
            screen,
            "Assets/graphics/Buttons/menu.png",
            "Assets/graphics/Buttons/menuP.png"
        )

class ExitButton(Button):
    def __init__(self, xMiddle, yMiddle, width, height, screen):
        super().__init__(
            xMiddle,
            yMiddle,
            width,
            height,
            screen,
            "Assets/graphics/Buttons/exit.png",      # normal image
            "Assets/graphics/Buttons/exitP.png"      # pressed / hover image
        )