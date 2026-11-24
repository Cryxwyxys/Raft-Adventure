import pygame
import os
import time
import json

import Buttons
import screens
import Games

pygame.init()

global sWidth 
global sHeight
global screenWidth
global screenHeight
info = pygame.display.Info()
screenHeight = info.current_h
screenWidth = info.current_w
sWidth = 0
sHeight = 0

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def loadScreenSettings():
    with open("settings.json", "r", encoding= "utf-8") as f:
        settings = json.load(f)
        if settings["fullscreen"]:
            info = pygame.display.Info()
            sWidth = screenWidth
            sHeight = screenHeight
        else:
            sWidth = settings["sWidth"]
            sHeight = settings["sHeight"]
        return [sWidth, sHeight]

def getJoystick():
    with open("settings.json", "r", encoding= "utf-8") as f:
        tDict = json.load(f)
        return tDict["usesJoystick"]

sSize = loadScreenSettings()
screen = pygame.display.set_mode(([sSize[0],sSize[1]]))
sWidth = sSize[0]
sHeight = sSize[1]
pygame.display.set_caption("Raft Game")

usesJoystick = False


if  __name__ == "__main__":
    instruction = [0]
    while True:
        match instruction[0]:
            case "start":
                p = Games.RunningGame(instruction[1], sWidth, sHeight, screen)
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
                instruction = screens.settingsScreen(sWidth, sHeight,  screen)
                if instruction[1] == True:
                    sSize = loadScreenSettings()
                    screen = pygame.display.set_mode(([sSize[0],sSize[1]]))
                    sWidth = sSize[0]
                    sHeight = sSize[1]

            case _ :            #default
                instruction = screens.startScreen(sWidth, sHeight, screen)