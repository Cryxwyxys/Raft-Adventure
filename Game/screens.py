import pygame
import Buttons

def startScreen(sWidth, sHeight, screen):

    startButton = Buttons.StartButton(sWidth / 2, sHeight / 4, sWidth / 5, sHeight / 8, screen)
    nameField = Buttons.TextField(sWidth / 2, sHeight / 2, sWidth / 5, sHeight / 8, screen)
    #scoreButton = Buttons.scoreButton(sWidth / 2, sHeight / 4 * 3, sWidth / 5, sHeight / 8, screen) # still have to write this one

    img = pygame.image.load('Assets/graphics/Screens/Title.jpg').convert()
    img = pygame.transform.scale(img,  (sWidth, sHeight))



    while True:
        screen.blit(img, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            nameField.handleEvent(event)

        nameField.render()
        startButton.render()
        pygame.display.update()
        if startButton.isClicked() and nameField.text != "": #prevents NULL-names to prevent score reading errors
            return ["start", nameField.text]
        #if scoreButton.isClicked(): return ["scores"]


def deathScreen(sWidth, sHeight, screen):

    img = pygame.image.load('Assets/graphics/Screens/death.png')
    img = pygame.transform.scale(img, (sWidth, sHeight))

    while True:
        screen.blit(img, (0,0))
        pygame.display.update()