import socket
import pickle
import os
from dotenv import load_dotenv

load_dotenv()

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = os.getenv('SERVER_IP')
        self.port = int(os.getenv('SERVER_PORT')) 
        self.addr = (self.server, self.port)
        self.id = self.connect()

    def getId(self):
        return self.id

    def connect(self):
        try:
            print("connecting")
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            msg = self.client.recv(2048*5)
            try:
                return pickle.loads(msg)
            except Exception as e:
                print(data)
                print(e)
                return None
        except socket.error as e:
            print(e)
