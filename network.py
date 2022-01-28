
import os
from dotenv import load_dotenv
import socket
import sys
import threading

load_dotenv()
class Peer:
    def __init__(self, ip, port, private_ip, private_port, id):
        self.id = id
        self.ip = ip
        self.port = port
        self.private_ip = private_ip
        self.private_port = private_port
        self.public = None
        self.last_update = None

class Network:
    def __init__(self):
        self.peers = []
        self.id = None

        print('connecting to server')

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        private_ip = s.getsockname()[0]
        s.close()

        self.sock.bind((private_ip, 0))
        server = os.getenv('SERVER_IP')
        port = int(os.getenv('SERVER_PORT'))
        self.server_address = (server,port)
        private_port = self.sock.getsockname()[1]
        self.sock.sendto("{} {}".format(private_ip, private_port).encode(), self.server_address)
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
            ip, port = address
            peer:Peer = list(filter(lambda p: (p.ip == ip and p.port == port) or (p.private_ip == ip and p.private_port == port), self.peers))
            if len(peer) > 0:
                peer = peer[0]
                if peer.public == None:
                    if ip == peer.private_ip:
                        self.public = False
                    elif ip == peer.ip:
                        self.public = True
                if len(data) > 5:
                    peer.last_update = data
            elif address == self.server_address:
                new_peers = []
                for peer in data.split(","):
                    ip, port, private_ip, private_port, id = peer.split(' ')
                    port = int(port)
                    private_port = int(private_port)
                    id = int(id)
                    new_peers.append(Peer(ip, port, private_ip, private_port, id))
                    if len(list(filter(lambda p: p.ip == ip and p.port == port, self.peers))) == 0:
                        self.sock.sendto(b'0',(ip, port))
                        self.sock.sendto(b'0', (private_ip, private_port))
                        print('\nJoined to game:')
                        print('  ip:          {}'.format(ip))
                        print('  port: {}'.format(port))
                        print('  private ip: {}'.format(private_ip))
                        print('  private port: {}'.format(private_port))
                        
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
                if peer.public == None:
                    self.sock.sendto(msg.encode(), (peer.ip, peer.port))
                    self.sock.sendto(msg.encode(), (peer.private_ip, peer.private_port))
                elif peer.public:
                    self.sock.sendto(msg.encode(), (peer.ip, peer.port))
                else:
                    self.sock.sendto(msg.encode(), (peer.private_ip, peer.private_port))
            except:
                print("error when sending a message")
                pass
    
    def end_session(self):
        try:
            self.sock.sendto("remove".encode(), self.server_address)
        except:
            pass

#n = Network(None)