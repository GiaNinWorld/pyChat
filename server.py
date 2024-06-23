import socket
import threading
import random

clients = []
nicknames = {}
colors = {}

# Lista de cores ANSI
color_codes = [
    '\033[91m',  # Vermelho
    '\033[92m',  # Verde
    '\033[93m',  # Amarelo
    '\033[94m',  # Azul
    '\033[95m',  # Magenta
    '\033[96m',  # Ciano
    '\033[97m',  # Branco
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
                nickname = nicknames[client_socket]
                color = colors[nickname]
                formatted_message = f"{color}{message.decode('utf-8')}\033[0m"
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
        broadcast(f"\n{color}{nickname} has joined the chat.\033[0m".encode('utf-8'), client_socket)
        client_socket.send("Connected to the server.".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
