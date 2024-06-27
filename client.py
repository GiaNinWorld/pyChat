import socket

from telanick import root as nickname_root
from testeinterfacedosguri import ChatDosGuri

def start_client(nickname):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('26.70.100.234', 5555))

    app = ChatDosGuri(client_socket, nickname)
    app.protocol("WM_DELETE_WINDOW", lambda: on_closing(client_socket, app))
    app.mainloop()

def on_closing(client_socket, app):
    client_socket.close()
    app.destroy()

if __name__ == "__main__":
    nickname_root.mainloop()  # Mostra a janela para inserção do nickname
    while not hasattr(nickname_root, 'nickname'):
        pass  # Aguarda até que nickname_root tenha o atributo nickname definido

    nickname = nickname_root.nickname  # Obtém o nickname inserido
    if nickname:
        start_client(nickname)
