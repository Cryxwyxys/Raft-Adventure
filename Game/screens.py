import pygame
import Buttons#
clock = pygame.time.Clock()

def startScreen(sWidth, sHeight, screen):

    startButton = Buttons.StartButton( sWidth / 2, sHeight / 4, sWidth / 5,sHeight / 8,screen)

    leaderboardButton = Buttons.LeaderboardButton(
        sWidth / 2,
        sHeight / 4 * 3,
        sWidth / 5,
        sHeight / 8,
        screen
    )

    nameField = Buttons.TextField(
        sWidth / 2,
        sHeight / 2,
        sWidth / 5,
        sHeight / 8,
        screen
    )

    img = pygame.image.load(
        'Assets/graphics/Screens/Title.jpg'
    ).convert()

    img = pygame.transform.scale(
        img,
        (sWidth, sHeight)
    )

    while True:

        screen.blit(img, (0, 0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            nameField.handleEvent(event)

        nameField.render()
        startButton.render()
        leaderboardButton.render()

        pygame.display.update()

        if startButton.isClicked() and nameField.text != "":
            return ["start", nameField.text]

        if leaderboardButton.isClicked():
            leaderboardScreen(sWidth, sHeight, screen)



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

import pygame
import Buttons
import os


def load_scores():

    scores = []

    try:
        with open("scores.txt", "r", encoding="utf-8") as file:

            for line in file:
                line = line.strip()

                if not line:
                    continue

                try:
                    name, score = line.split("-", 1)
                    scores.append((name, int(score)))
                except ValueError:
                    continue

    except FileNotFoundError:
        pass

    # Highest score first
    scores.sort(key=lambda x: x[1], reverse=True)

    return scores


def leaderboardScreen(sWidth, sHeight, screen):

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 60)
    scoreFont = pygame.font.Font(None, 45)
    titleFont = pygame.font.Font(None, 100)

    menuButton = Buttons.MenuButton(
        sWidth / 2,
        sHeight - 100,
        300,
        100,
        screen
    )

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Check button
        if menuButton.isClicked():
            return

        # Background
        screen.fill("SKYBLUE")

        # Title
        title = titleFont.render(
            "LEADERBOARD",
            True,
            "WHITE"
        )

        titleRect = title.get_rect(
            center=(sWidth / 2, 100)
        )

        screen.blit(title, titleRect)

        # Get scores
        scores = load_scores()

        # Display top 10
        y = 220

        for i, (name, score) in enumerate(scores[:10]):

            text = scoreFont.render(
                f"{i + 1}. {name}     {score}",
                True,
                "WHITE"
            )

            textRect = text.get_rect(
                center=(sWidth / 2, y)
            )

            screen.blit(text, textRect)

            y += 60

        # No scores message
        if not scores:

            text = scoreFont.render(
                "No scores yet!",
                True,
                "WHITE"
            )

            textRect = text.get_rect(
                center=(sWidth / 2, 300)
            )

            screen.blit(text, textRect)

        menuButton.render()

        pygame.display.update()

        clock.tick(60)
