
import os
from dotenv import load_dotenv
import socket
import sys
import threading

load_dotenv()
class Peer:
    def __init__(self, ip, port, id):
        self.id = id
        self.ip = ip
        self.port = port

class Network:
    def __init__(self, game):
        self.peers = []
        self.game = game
        self.id = None
        print('connecting to server')

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 0))
        server = os.getenv('SERVER_IP')
        port = int(os.getenv('SERVER_PORT'))
        self.server_address = (server,port)
        self.sock.sendto(b'0', self.server_address)
        self.listeners = []
        self.connected = False

        while True:
            data = self.sock.recv(1024).decode()

            self.id = int(data)
            print('checked in with server')
            break
        
        self.listener = threading.Thread(target=self.listen, daemon=True)
        self.listener.start()

    def getId(self):
        return self.id

    def listen(self):
        while True:
            try:
                data, address = self.sock.recvfrom(1024)
            except:
                continue
            data = data.decode()
            ip, port = address
            peer = list(filter(lambda p: p.ip == address[0] and p.port == port, self.peers))
            if len(peer) > 0:
                peer = peer[0]
                self.game.update_game_state(data)
            elif address == self.server_address:
                new_peers = []
                for peer in data.split(","):
                    ip, port, id = peer.split(' ')
                    port = int(port)
                    id = int(id)
                    new_peers.append(Peer(ip, port, id))
                    if len(list(filter(lambda p: p.ip == ip and p.port == port, self.peers))) == 0:
                        print('\nJoined to game:')
                        print('  ip:          {}'.format(ip))
                        print('  source port: {}'.format(port))
                self.peers = new_peers
            
    #def send(self):
    #    while True:
    #        msg = input('> ')
    #        for peer in self.peers:
    #            try:
    #                self.sock.sendto(msg.encode(), (peer.ip, peer.port))
    #            except:
    #                pass

    def send(self, msg):
        for peer in self.peers:
            try:
                self.sock.sendto(msg.encode(), (peer.ip, peer.port))
            except:
                pass

#n = Network(None)