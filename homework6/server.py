import socket
import threading

host = '192.168.43.1'
port = 60000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left the chat!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print("Nickname is {}".format(nickname))
        broadcast("{} joined the chat!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...")
receive()
