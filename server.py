import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 5555))

clientId = 1

print("Waiting for connection...")

while True:
    clients = []

    while True:
        try:
            data, address = sock.recvfrom(128)
        except:
            continue
        msg = data.decode()
        if msg == "remove":
            print('{} left the room'.format(address))
            clients = list(filter(lambda c: (c[0], c[1]) != address, clients))
        else:
            private_ip, private_port = msg.split(" ")
            print('connection from: {}'.format(address))
            clients.append(address + (private_ip, private_port, clientId))

            sock.sendto('{}'.format(clientId).encode(), address)
            clientId += 1

        for client in clients:
            message = ""
            for client2 in clients:
                if client2 != client:
                    addr, port, private_ip, private_port, id = client2
                    message += '{} {} {} {} {},'.format(addr, port, private_ip, private_port, id)
            if len(message) > 5:
                message = message[:-1]
                sock.sendto(message.encode(), (client[0], client[1]))