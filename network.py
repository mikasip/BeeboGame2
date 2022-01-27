
import os
from dotenv import load_dotenv
import socket
import sys
import threading

load_dotenv()
class Peer:
    def __init__(self, ip, port, sending_port, id):
        self.id = id
        self.ip = ip
        self.port = port
        self.sending_port = sending_port
        self.last_update = None

class Network:
    def __init__(self):
        self.peers = []
        self.id = None

        print('connecting to server')

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 0))
        self.sending_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sending_sock.bind(('0.0.0.0', 0))
        server = os.getenv('SERVER_IP')
        port = int(os.getenv('SERVER_PORT'))
        self.server_address = (server,port)
        self.sock.sendto(str(self.sending_sock.getsockname()[1]).encode(), self.server_address)
        self.listeners = []
        self.connected = False

        while True:
            try:
                data = self.sock.recv(1024).decode()
                self.id = int(data)
                print('checked in with server')
                break
            except:
                print('connection failed')
                break
        
        self.listener = threading.Thread(target=self.listen, daemon=True)
        self.listener.start()

    def getId(self):
        return self.id
    
    def getMessages(self):
        messages = []
        for peer in self.peers:
            if peer.last_update != None:
                messages.append(peer.last_update)
                peer.last_update = None
        return messages

    def listen(self):
        while True:
            try:
                data, address = self.sock.recvfrom(1024)
            except:
                print("error when receiving a message")
                continue
            data = data.decode()
            ip, sending_port = address
            peer = list(filter(lambda p: p.ip == ip and p.sending_port == sending_port, self.peers))
            if len(peer) > 0:
                peer = peer[0]
                peer.last_update = data
            elif address == self.server_address:
                new_peers = []
                for peer in data.split(","):
                    ip, port, sending_port, id = peer.split(' ')
                    port = int(port)
                    sending_port = int(sending_port)
                    id = int(id)
                    new_peers.append(Peer(ip, port, sending_port, id))
                    if len(list(filter(lambda p: p.ip == ip and p.port == port, self.peers))) == 0:
                        self.sock.sendto(b'0',(ip, sending_port))
                        print('\nJoined to game:')
                        print('  ip:          {}'.format(ip))
                        print('  destination port: {}'.format(port))
                        print('  sending port: {}'.format(sending_port))
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
                self.sending_sock.sendto(msg.encode(), (peer.ip, peer.port))
            except:
                print("error when sending a message")
                pass
    
    def end_session(self):
        try:
            self.sock.sendto("remove".encode(), self.server_address)
        except:
            pass

#n = Network(None)