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

    def render(self):
        super().render()


class TextField(Button): # Vibe-Coded

    def __init__(self, xMiddle, yMiddle, width, height, screen):
        self.text = "Enter Name"
        self.font = pygame.font.SysFont(None, 36)
        self.active = False   #checks if textinput should go in that field
        displaytext = self.font.render(self.text, True, 'BLACK')
        textRect = displaytext.get_rect()

        super().__init__(xMiddle, yMiddle, textRect.width + 200, height, screen,
                          'Assets/graphics/Buttons/textField.png', "Assets/graphics/Buttons/textField.png")

    def checkHovering(self):
        super().checkHovering()

    def handleEvent(self, event): # needs to be put in the for pygame.event.get loop
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)   #checks if the field has been selectet

        elif self.active and event.type == pygame.KEYDOWN:    #checks for backspace
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]                    #removes last char from string

        elif self.active and event.type == pygame.TEXTINPUT:
            if self.text == "Enter Name": self.text = ""      #QoS might optemise later 
            self.text += event.text                           #adds textinput to text

    def render(self):
        super().render()  # zeichnet weiterhin imgN/imgP
        displaytext = self.font.render(self.text, True, 'BLACK')
        textRect = displaytext.get_rect(center=self.rect.center)
        self.screen.blit(displaytext, textRect)





if __name__ == "__main__":
    import time # for debugging, can probably removed in the end
    import os

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Raft1")
    testbutton = RestartButton(50, 50 , 100, 100, screen)
    while True: 
        


        testbutton.render()
        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        if testbutton.isClicked():
            print("testButton")
            
class LeaderboardButton(Button):

    def __init__(self, xMiddle, yMiddle, width, height, screen):
        super().__init__(xMiddle,
            yMiddle,
            width,
            height,
            screen,
            "Assets/graphics/Buttons/leaderboard.png",
            "Assets/graphics/Buttons/leaderboardP.png"
        )

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


