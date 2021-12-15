import pygame
import time
from random import randint
from network import Network

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

## PLAYER
f1 = (1,pygame.image.load('otse0.png'))
f2 = (2,pygame.image.load("otse1.png"))
f3 = (3,pygame.image.load("otse2.png"))
r1 = (4,pygame.image.load("parem0.png"))
r2 = (5,pygame.image.load("parem1.png"))
r3 = (6,pygame.image.load("parem2.png"))
l1 = (7,pygame.image.load("vasak0.png"))
l2 = (8,pygame.image.load("vasak1.png"))
l3 = (9,pygame.image.load("vasak2.png"))
b1 = (10,pygame.image.load("tagasi0.png"))
b2 = (11,pygame.image.load("tagasi1.png"))
b3 = (12,pygame.image.load("tagasi2.png"))

## player sprite
playerIcon = f1
forward = [f1, f2, f3]
right = [r1, r2, r3]
left = [l1, l2, l3]
backwards = [b1, b2, b3]
i = 0

p2Images = [f1,f2,f3,r1,r2,r3,l1,l2,l3,b1,b2,b3]

p1Current = 0
p2Current = 0
player2Icon = p2Images[p2Current]

## player coordinates
player2X = 0
player2Y = 0
change = 0.06

## player function
def player(sprite, x, y):
    screen.blit(sprite, (x, y))

def read_pos(s):
    s = s.split(",")
    return int(s[0]), float(s[1]), float(s[2]), int(s[3])

def make_pos(sprite ,x, y, value):
    return str(sprite) + ',' + str(x) + ',' + str(y) + ',' + str(value)

## background
background = pygame.image.load("background.png")

## win/lose window
win = pygame.image.load("win.png")
lose = pygame.image.load("lose.png")

startTime = time.time()
didPlayerLose = False

## game loop
running = True
n = Network()
startPos = n.getPos().split(',')
player1X = float(startPos[1])
player1Y = float(startPos[2])

while running:

    for x in range(0, len(p2Images)):
        if playerIcon[0] in p2Images[x]:
            p1Current = p2Images[x][0]

    p2Pos = read_pos(n.send(make_pos(p1Current, player1X, player1Y, int(isItGreen))))
    player2X = p2Pos[1]
    player2Y = p2Pos[2]

    if player1Y < 89:

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

        print(p2Pos)
        if p2Pos[3] != int(isItGreen):
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
            player1X -= change
            i += 0.01
            if i >= len(left):
                i = 0
            playerIcon = left[int(i)]
        elif key[pygame.K_RIGHT]:
            player1X += change
            i += 0.01
            if i >= len(right):
                i = 0
            playerIcon = right[int(i)]
        elif key[pygame.K_UP]:
            player1Y -= change
            i += 0.01
            if i >= len(forward):
                i = 0
            playerIcon = forward[int(i)]
        elif key[pygame.K_DOWN]:
            player1Y += change
            fw = False
            i += 0.01
            if i >= len(backwards):
                i = 0
            playerIcon = backwards[int(i)]
        if player1X <= 0:
            player1X = 0
        elif player1X >= 975:
            player1X = 975

        if player1Y <= 0:
            player1Y = 0
        elif player1Y >= 755:
            player1Y = 755

        if isItGreen:
            doll(greenLight, dollX, dollY)
        elif not isItGreen:
            doll(redLight, dollX, dollY)

        for x in range(0, len(p2Images)):
            if p2Pos[0] == p2Images[x][0]:
                player2Icon = p2Images[x]

        player(playerIcon[1], player1X, player1Y)
        player(player2Icon[1], player2X, player2Y)
        pygame.display.update()
