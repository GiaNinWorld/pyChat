import socket
import threading
import os

emoji_dict = {
    ":)" : "😊",
    ":(" : "😞",
    ":D" : "😀",
    ":O" : "😲",
    ":P" : "😛",
    ":|" : "😐",
    ":3" : "🤪",
    ":/" : "🙄",
    ":>" : "😁",
    ":<" : "🙁",
}

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'NICKNAME':
                client_socket.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client_socket.close()
            break

def send_messages(client_socket):
    while True:
        message_input = replace_emojis(input(""))
        message = f'\n[{nickname}]:\n  {message_input}'
        client_socket.send(message.encode('utf-8'))

def replace_emojis(message):
    for key, value in emoji_dict.items():
        message = message.replace(key, value)
    return message

def send_file(client_socket, file_path):
    if os.path.getsize(file_path) > 20 * 1024 * 1024:  # 20 MB
        print("File size exceeds 20 MB limit.")
        return

    client_socket.send('file'.encode('utf-8'))
    file_name = os.path.basename(file_path)
    client_socket.send(file_name.encode('utf-8'))
    file_size = str(os.path.getsize(file_path))
    client_socket.send(file_size.encode('utf-8'))

    with open(file_path, 'rb') as file:
        while chunk := file.read(1024):
            client_socket.send(chunk)
    print("File sent successfully.")

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('26.70.100.234', 5555))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    choice = input("Digite 'm' para enviar mensagem ou 'f' para enviar arquivo: ")
    
    if choice.upper() == 'F':
        file_path = input("Digite o caminho do arquivo a ser enviado: ")
        send_file(client_socket, file_path)
    else:
        send_thread = threading.Thread(target=send_messages, args=(client_socket,))
        send_thread.start()
        
if __name__ == "__main__":
    nickname = input("Choose your nickname: ")
    start_client()
