#!/usr/bin/env python3
import socket
from _thread import *
from GameState import GameState
import pickle
import os
from dotenv import load_dotenv

load_dotenv()

server = os.getenv('SERVER_IP')
port = int(os.getenv('SERVER_PORT'))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(10)
print("Waiting for a connection, Server Started")

connected = set()
game = None
idCount = 0

def threaded_client(conn, playerId):
    global idCount
    conn.send(str.encode(str(playerId)))

    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            if game != None:
                if len(data) == 0:
                    break
                else:
                    try:
                        for state in data:
                            if state != "get":
                                game.updateState(state)
                    except Exception as e:
                        print(e)

                conn.send(pickle.dumps(game))
            else:
                break
        except Exception as e:
            print(e)
            break

    print("Lost connection")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    playerId = idCount
    idCount += 1
    if game == None:
        game = GameState()

    start_new_thread(threaded_client, (conn, playerId))