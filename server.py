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
            print('connection from: {}'.format(address))
            clients.append(address + (msg, clientId))

            sock.sendto('{}'.format(clientId).encode(), address)
            clientId += 1

        for client in clients:
            message = ""
            for client2 in clients:
                if client2 != client:
                    addr, port, sending_port, id = client2
                    message += '{} {} {} {},'.format(addr, port, sending_port, id)
            if len(message) > 1:
                message = message[:-1]
                sock.sendto(message.encode(), (client[0], client[1]))