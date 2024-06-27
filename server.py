import os
import socket
import random
import threading

colors = {}
clients = []
nicknames = {}

# Lista de cores em hexadecimal
color_codes = [
    '#FF5733',
    '#402E7A',
    '#4B70F5',
    '#FF33FF',
    '#3DC2EC',
    '#647E68',
    '#041C32',
    '#8B9A46',
    '#4E9F3D'
]

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                if message.startswith(b'FILE:'):
                    filename = message[5:].decode('utf-8')
                    filepath = os.path.join(os.getcwd(), filename)
                    with open(filepath, 'wb') as f:
                        while True:
                            data = client_socket.recv(1024)
                            if not data:
                                break
                            f.write(data)
                    broadcast(f"Arquivo recebido: {filename}".encode('utf-8'), client_socket)
                else:
                    nickname = nicknames[client_socket]
                    color = colors[nickname]
                    formatted_message = f"{nickname}:{color}:{message.decode('utf-8')}"
                    print(formatted_message)
                    broadcast(formatted_message.encode('utf-8'), client_socket)
        except:
            nickname = nicknames[client_socket]
            broadcast(f"\n{nickname} has left the chat.".encode('utf-8'), client_socket)
            print(f"{nickname} has disconnected.")
            clients.remove(client_socket)
            del nicknames[client_socket]
            del colors[nickname]
            client_socket.close()
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))  # Ouvir em todas as interfaces de rede
    server.listen()
    print("Server is listening on port 5555")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_socket.send("NICKNAME".encode('utf-8'))
        nickname = client_socket.recv(1024).decode('utf-8')
        nicknames[client_socket] = nickname
        clients.append(client_socket)

        # Atribuir uma cor aleatória ao nickname
        color = random.choice(color_codes)
        colors[nickname] = color

        print(f"New client connected {nickname}")
        broadcast(f"\n{nickname} has joined the chat.\n".encode('utf-8'), client_socket)
        client_socket.send("Connected to the server.".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
