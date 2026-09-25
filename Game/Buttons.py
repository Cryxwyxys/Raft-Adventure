# buttons for menu screens

import pygame
import os
import time # for debugging, can probably removed in the end

pygame.init()


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

    def isClicked(self):
        mousePos = pygame.mouse.get_pos()
        
        self.hovering = self.rect.collidepoint(mousePos)
        print(self.hovering)
        self.down = pygame.mouse.get_pressed()[0]
        print(self.down)
        return self.hovering and self.down

    def render(self):
        screen.blit(self.surface, self.rect)



p = Button(50, 50 , 100, 100, "Assets/graphics/Buttons/redButton.png")
p.render()

pygame.display.update()

print(p.isClicked())

while True: 
    t = pygame.mouse.get_pos()
    print(t)
