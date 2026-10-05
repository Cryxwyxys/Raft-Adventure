# buttons for menu screens

import pygame
import os


class Button():
    
    def __init__(self, xMiddle, yMiddle, width, height, screen, normalImg, hoveringImg):
        self.xMiddle = xMiddle
        self.yMiddle = yMiddle
        self.width = width
        self.height = height
        self.imgN = pygame.image.load(normalImg).convert()
        self.imgP = pygame.image.load(hoveringImg).convert()
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
        




if __name__ == "__main__":
    import time # for debugging, can probably removed in the end
    
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Raft1")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    testbutton = Button(50, 50 , 100, 100, screen, "Assets/graphics/Buttons/redButton.png", "Assets/graphics/Buttons/redButtonPressed.png")
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

