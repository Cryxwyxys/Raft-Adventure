import pygame
import os
import time
import json

import Buttons
import screens
import Games

global sWidth 
global sHeight
sWidth = 0
sHeight = 0

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

def loadSettings():
    with open("settings.json", "r", encoding= "utf-8") as f:
        settings = json.load(f)
        if settings["fullscreen"]:
            info = pygame.display.Info()
            sWidth = info.current_w
            print(sWidth)
            sHeight = info.current_h
        else:
            sWidth = settings["sWidth"]
            sHeight = settings["sHeight"]
        screen = pygame.display.set_mode((sWidth, sHeight))
        return screen

screen = loadSettings()
info = pygame.display.Info()
sWidth = info.current_w
sHeight = info.current_h
print(screen)
pygame.display.set_caption("Raft Game")




# if(pygame.joystick.get_count()):
#     pygame.joystick.init()
#     joystick = pygame.joystick.Joystick(0)
#     joystick.init()
#     usesJoystick = True

# else:
usesJoystick = False

 
if  __name__ == "__main__":
    instruction = [0]
    loadSettings()
    while True:
        match instruction[0]:
            case "start":
                p = Games.RunningGame(instruction[1], sWidth, sHeight, screen, usesJoystick)
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

            case "settings":
                instruction = screens.settingsScreen(sWidth, sHeight, screen)
                if instruction[1] == True:
                    screen = loadSettings()
                    info = pygame.display.Info()
                    sWidth = info.current_w
                    sHeight = info.current_h

            case _ :            #default
                print(sWidth)
                instruction = screens.startScreen(sWidth, sHeight, screen)