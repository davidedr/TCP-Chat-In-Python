import socket
import threading
import sys

server_address = 'localhost'
server_port = 55555

nickname = input("Choose your nickname:")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_address, server_port))

def receive():
    print("Receive thread ready.")
    while True:
        try:
            message = client_socket.recv(1024).decode('ascii')
            if message=="NICK?":
                client_socket.send(nickname.encode('ascii'))
            else:
                print(message)
        except Exception as e:
            print("receive: An error occurred!", file=sys.stderr)
            print(e)
            client_socket.close()
            break

    print("Receiver thread ends.")

def write():
    print("Writer thread ready.")
    nmsgs = 0
    while True:
        message = input("Say something...")
        nmsgs = nmsgs+1
        print("write msg n.: {}".format(nmsgs), client_socket)         
        client_socket.send(message.encode('ascii'))
        if message.startswith('#quit'):
            client_socket.close()
            break  

    print("Writer thread ends.")

receive_thread = threading.Thread(target = receive)
receive_thread.start()

writing_thread = threading.Thread(target = write)
writing_thread.start()