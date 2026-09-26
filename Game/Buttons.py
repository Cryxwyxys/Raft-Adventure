# buttons for menu screens

import pygame
import os
import time # for debugging, can probably removed in the end

pygame.init()


clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 1000))

pygame.display.set_caption("Raft1")

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Button():
    
    def __init__(self, xMiddle, yMiddle, width, height, surface):
        self.xMiddle = xMiddle
        self.yMiddle = yMiddle
        self.width = width
        self.height = height
        self.surface = pygame.image.load('Assets/graphics/Buttons/redButton.png').convert()

        self.rect = pygame.Rect(xMiddle - width / 2, yMiddle - height / 2, width, height)
        self.surface = pygame.transform.scale(self.surface, (self.width, self.height))

    def isHovering(self):
        mousePos = pygame.mouse.get_pos()
        self.hovering = self.rect.collidepoint(mousePos)

    def displayHover(self):
        self.greyOverlay = pygame.surface(self.width, self.height)
        if isHovering():
            self.greyoverlay


    def isClicked(self):
        mousePos = pygame.mouse.get_pos()
        
        self.hovering = self.rect.collidepoint(mousePos)
        self.down = pygame.mouse.get_pressed()[0]
        return self.hovering and self.down

    def render(self):
        screen.blit(self.surface, self.rect)
        
        pygame.draw.rect(screen, 'BLACK', self.rect, 5)
        pygame.draw.rect(screen, 'RED', self.rect, 2)



testbutton = Button(50, 50 , 100, 100, "Assets/graphics/Buttons/redButton.png")
testbutton.render()

pygame.display.update()

if __name__ == "__main__":
    while True: 

        testbutton.render()
        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        if testbutton.isClicked():

            exit()

