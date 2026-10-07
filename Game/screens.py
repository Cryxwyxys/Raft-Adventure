import pygame
import Buttons#
clock = pygame.time.Clock()

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


def deathScreen(sWidth, sHeight, raft, name, screen):
    background = pygame.image.load('Assets/graphics/Screens/background.png')

    img = pygame.image.load('Assets/graphics/Screens/death.png')
    img = pygame.transform.scale(img, (sWidth, sHeight))

    raft.hitbox.centery -= 600

    for i in range(60):
        screen.blit(background, (0,0))
        raft.hitbox.centery += 3
        img.set_alpha(i * 5)
        screen.blit(img, (0, 0))
        screen.blit(raft.img, raft.hitbox)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        clock.tick(60)
    
    restartButton = Buttons.RestartButton(sWidth / 4, sHeight / 3 * 2, sWidth  / 6, sHeight / 5 *3, screen)

    while True:
        screen.blit(img, (0,0))
        restartButton.render()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        if restartButton.isClicked():
            print("fuck")
            return ["restart",name]