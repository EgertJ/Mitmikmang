import pygame
import time
from random import randint

pygame.init()

## creates the screen
screen = pygame.display.set_mode((1000, 800))

## icon
icon = pygame.image.load('sds.png')
pygame.display.set_icon(icon)

## title
pygame.display.set_caption("Red light")

## green light or red light boolean
isItGreen = False

## doll sprites
redLight = pygame.image.load('redlight.png')
greenLight = pygame.image.load('greenlight.png')

## doll coordinates
dollX = 472
dollY = 30

## doll function
def doll(sprite, x, y):
    screen.blit(sprite, (x, y))

## doll sounds
green_sound = pygame.mixer.Sound("greenlight.mp3")
red_sound = pygame.mixer.Sound("redlight.mp3")

## player sprite
playerIcon = pygame.image.load('otse0.png')

## player coordinates
playerX = randint(0, 945)
playerY = 700
change = 0.06

## player function
def player(x, y):
    screen.blit(playerIcon, (x, y))

## background
background = pygame.image.load("background.png")

## win/lose window
win = pygame.image.load("win.png")
lose = pygame.image.load("lose.png")

# red light / green light switch
lightSwitch = pygame.USEREVENT + 0
pygame.time.set_timer(lightSwitch, randint(2500,10000))

startTime = time.time()
didPlayerLose = False

## game loop
running = True
while running:
    
    if playerY < 89:

        screen.fill((0,0,0))
        screen.blit(win, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()

    elif didPlayerLose:
        
        screen.fill((0,0,0))
        screen.blit(lose, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()

    else:

        screen.fill((0,0,0))
        screen.blit(background, (0,0))

        ## if game is closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == lightSwitch:
                pygame.time.set_timer(lightSwitch, randint(2500, 10000))
                isItGreen = not isItGreen
                if isItGreen:
                    pygame.mixer.Sound.play(green_sound)
                elif not isItGreen:
                    startTime = round(time.time(), 1)
                    pygame.mixer.Sound.play(red_sound)
        
        key = pygame.key.get_pressed()
        
        if not isItGreen:
            if round(time.time(), 1) > float(startTime) + 0.5:
                if key[pygame.K_LEFT] or key[pygame.K_RIGHT] or key[pygame.K_UP] or key[pygame.K_DOWN]:
                    didPlayerLose = True

        if key[pygame.K_LEFT]:
            playerX -= change
        elif key[pygame.K_RIGHT]:
            playerX += change
        elif key[pygame.K_UP]:
            playerY -= change
        elif key[pygame.K_DOWN]:
            playerY += change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 975:
            playerX = 975
        
        if playerY <= 0:
            playerY = 0
        elif playerY >= 755:
            playerY = 755

        if isItGreen:
            doll(greenLight, dollX, dollY)
        elif not isItGreen:
            doll(redLight, dollX, dollY)

        player(playerX, playerY)
        pygame.display.update()