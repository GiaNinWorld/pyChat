import socket
import threading

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

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5555))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

if __name__ == "__main__":
    nickname = input("Choose your nickname: ")
    start_client()
