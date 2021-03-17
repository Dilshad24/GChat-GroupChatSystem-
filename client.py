import threading
import socket

host = '127.0.0.1'
port = 55555
decode_format = 'ascii'
msg_size=1024
nickname = input("choose the nickname: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def receive():
    while True:
        try:
            message = client.recv(msg_size).decode(decode_format)

            if message == "NICK":
                client.send(nickname.encode(decode_format))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}:{input("")}'
        client.send(message.encode(decode_format))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()