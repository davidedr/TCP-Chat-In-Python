import socket
import threading
import sys

server_address = 'localhost'
server_port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET= internet socket (as opposed to unix socket); SOCK_STREAM = TCP socket
server.bind((server_address, server_port))
server.listen();

clients = []
nicknames = []

def broadcast(message, sender = None):
    for client in clients:
        if sender:
            if client != sender:
                client.send(message.encode('ascii'))
        else:
            client.send(message.encode('ascii'))

def handle(client):
    index = clients.index(client)
    nickname = nicknames[index]

    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message.startswith("#list"):
                client.send(str(nicknames).encode('ascii'))
            elif message.startswith("#quit"):
                clients.remove(client)
                client.close()
                broadcast('{} left!'.format(nickname))
                nicknames.remove(nickname)
                print("{} left.".format(nickname))
                break
            else:
                broadcast("{}: {}".format(nickname, message), client)

        except Exception as e:
            print("handle: exception raised!", file = sys.stderr)
            print(e)
            clients.remove(client)
            client.close()
            broadcast('{} left!'.format(nickname))
            nicknames.remove(nickname)
            print("{} left.".format(nickname))
            break
    print("handle for: {} ends.".format(nickname), file = sys.stderr)

def receive():
    print("Starting server on {} {}...".format(server_address, server_port), file = sys.stderr)
    while True:
        client, address = server.accept()

        # Ask for and store nickname
        client.send("NICK?".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        print("Connected w/: {}, nickname: {}.".format(str(address), nickname), file = sys.stderr)
        nicknames.append(nickname)
        clients.append(client)

        join_message = "{} joined.".format(nickname)
        print(join_message)
        broadcast(join_message)
        client.send("{}: you're connected!".format(nickname).encode('ascii'))

        thread = threading.Thread(target = handle, args = (client, ))
        thread.start()

receive()