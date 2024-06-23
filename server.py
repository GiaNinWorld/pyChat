import socket
import threading

clients = []
nicknames = {}

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
                print(f"Received message\n{message.decode('utf-8')}")
                broadcast(message, client_socket)
        except:
            nickname = nicknames[client_socket]
            broadcast(f"{nickname} has left the chat.".encode('utf-8'), client_socket)
            print(f"{nickname} has disconnected.")
            clients.remove(client_socket)
            del nicknames[client_socket]
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
        print(f"New client connected {nickname}")
        broadcast(f"{nickname} has joined the chat.".encode('utf-8'), client_socket)
        client_socket.send("Connected to the server.".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
