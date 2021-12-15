import socket
import pygame
from _thread import *
from random import randint
import sys

pygame.init()

server = '192.168.1.176'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# red light / green light switch
lightSwitch = pygame.USEREVENT + 1
pygame.time.set_timer(lightSwitch, randint(2500, 10000))
## green light or red light boolean
isItGreen = False

s.listen(2)
print('Waiting for connection, server started')

def read_pos(s):
    s = s.split(",")
    return int(s[0]), float(s[1]), float(s[2]), int(s[3])

def make_pos(tup):
    return str(tup[0]) + ',' + str(tup[1]) + ',' + str(tup[2]) + ',' + str(tup[3])

pos = [(0, randint(0, 945), 700, 0),(0, randint(0, 945), 700, 0)]

def threaded_client(conn, player):

    global isItGreen

    conn.send(str.encode(make_pos(pos[player])))
    reply = ''
    while True:

        for event in pygame.event.get():
            if event.type == lightSwitch:
                pygame.time.set_timer(lightSwitch, randint(2500, 10000))
                isItGreen = not isItGreen

        data = read_pos(conn.recv(2048).decode())
        data = (data[0], data[1], data[2], int(isItGreen))
        pos[player] = (data[0], data[1], data[2], data[3])
        reply = data

        if not data:
            print('Disconnected')
            break
        else:
            if player == 1:
                reply = pos[0]
            else:
                reply = pos[1]

            print('Received:', data)
            print('Sending: ', reply)

        conn.sendall(str.encode(make_pos(reply)))

    print('Lost connection')
    conn.close()

currentPlayer = 0

while True:
    conn, addr = s.accept()
    print('Connected to:', addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1