import os
import threading
import tkinter as tk
from PIL import Image
import customtkinter as ctk
from tkinter import filedialog, simpledialog

file_path = os.path.dirname(os.path.realpath(__file__))
image_1 = ctk.CTkImage(Image.open(file_path + './assets/baixar.png'), size=(20,20))

def receive_messages(client_socket, gui):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith('FILE:'):
                filename = message[5:]
                filepath = os.path.join(file_path, filename)
                with open(filepath, 'wb') as f:
                    while True:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        f.write(data)
                gui.show_message("Arquivo recebido:", "blue", filename)
            elif message == 'NICKNAME':
                client_socket.send(gui.nickname.encode('utf-8'))
            else:
                parts = message.split(':', 2)
                if len(parts) == 3:
                    sender, color, text = parts
                    gui.show_message(sender, color, text)
        except:
            print("An error occurred!")
            client_socket.close()
            break

class ChatDosGuri(ctk.CTk):
    def __init__(self, client_socket):
        super().__init__()

        self.client_socket = client_socket
        self.nickname = simpledialog.askstring('Nickname', 'Escolha seu apelido', parent=self)

        self.title("Chat dos Guri")
        self.geometry("1280x720")

        self.frame_chat = ctk.CTkFrame(self)
        self.frame_chat.pack(expand=True, fill=tk.BOTH, padx=15, pady=15)

        self.area_texto = tk.Text(self.frame_chat, state='disabled', wrap='word')
        self.area_texto.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.entrada = ctk.CTkEntry(self, placeholder_text="Digite sua mensagem.")
        self.entrada.pack(side=tk.LEFT, fill=tk.X, padx=15, pady=12, expand=True)
        self.entrada.bind("<Return>", self.enviar_mensagem)

        self.botao_enviar = ctk.CTkButton(self, text="Enviar", fg_color='#111111', command=self.enviar_mensagem)
        self.botao_enviar.pack(side=tk.LEFT, padx=10, pady=10)

        self.botao_anexar = ctk.CTkButton(self, text="Anexar Arquivo", fg_color='#111111', command=self.anexar_arquivo)
        self.botao_anexar.pack(side=tk.RIGHT, padx=10, pady=10)

        self.receive_thread = threading.Thread(target=receive_messages, args=(self.client_socket, self))
        self.receive_thread.start()

    def show_message(self, sender, color, message):
        self.area_texto.configure(state='normal')
        self.area_texto.insert(tk.END, f"{sender}:\n", ('nickname',))
        self.area_texto.insert(tk.END, f"{message}\n", ('message',))
        self.area_texto.tag_config('nickname', foreground=color)
        self.area_texto.configure(state='disabled')
        self.area_texto.yview(tk.END)

    def get_message(self):
        mensagem = self.entrada.get()
        if mensagem.strip():
            self.area_texto.configure(state='normal')
            self.area_texto.insert(tk.END, f"Você: {mensagem}\n")
            self.area_texto.configure(state='disabled')
            self.entrada.delete(0, tk.END)
            self.area_texto.yview(tk.END)
            return mensagem
        return None

    def enviar_mensagem(self, event=None):
        mensagem = self.get_message()
        if mensagem:
            self.client_socket.send(f'  {mensagem}\n'.encode('utf-8'))

    def anexar_arquivo(self):
        caminho_arquivo = filedialog.askopenfilename()
        if caminho_arquivo:
            nome_arquivo = os.path.basename(caminho_arquivo)
            self.client_socket.send(f'FILE:{nome_arquivo}'.encode('utf-8'))
            with open(caminho_arquivo, 'rb') as f:
                while True:
                    bytes_read = f.read(1024)
                    if not bytes_read:
                        break
                    self.client_socket.send(bytes_read)

            self.area_texto.configure(state='normal')
            self.area_texto.insert(tk.END, f"{nome_arquivo} ")
            self.area_texto.insert(tk.END, "\n")
            self.area_texto.configure(state='disabled')
            self.area_texto.yview(tk.END)

if __name__ == "__main__":
    app = ChatDosGuri(None)
    app.mainloop()
