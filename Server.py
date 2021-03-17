import threading
import socket
from datetime import datetime
host = '127.0.0.1'
port = 55555
decode_format = 'ascii'
msg_size = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []
def brodcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(msg_size)
            brodcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            brodcast(f"{nickname} left the chat!".encode(decode_format))
            nicknames.remove(nickname)
            break

def recieve():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")
        client.send('NICK'.encode(decode_format))
        nickname = client.recv(msg_size).decode(decode_format)
        nicknames.append(nickname)
        clients.append(client)
        print(f"nick name of client is {nickname}!")
        brodcast(f'{nickname} joined the chat\n'.encode(decode_format))
        client.send('connected to the server'.encode(decode_format))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")
print( " server is listening.... " )
recieve()


