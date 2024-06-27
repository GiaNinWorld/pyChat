import os
import random
import tkinter as tk
from PIL import Image
import customtkinter as ctk
from tkinter import filedialog

file_path = os.path.dirname(os.path.realpath(__file__))
image_1 = ctk.CTkImage(Image.open(file_path + './assets/baixar.png'), size=(25,25))


class ChatDosGuri(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Chat dos Guri")
        self.geometry("1280x720")

        # tela para exibir mensagens
        self.frame_chat = ctk.CTkFrame(self)
        self.frame_chat.pack(expand=True, fill=tk.BOTH, padx=15, pady=15)

        # Widget de texto para mostrar mensagens
        self.area_texto = tk.Text(self.frame_chat, state='disabled', wrap='word')
        self.area_texto.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Widget para digitar novas mensagens
        self.entrada = ctk.CTkEntry(self, placeholder_text="Digite sua mensagem.")
        self.entrada.pack(side=tk.LEFT, fill=tk.X, padx=15, pady=12, expand=True)
        self.entrada.bind("<Return>", self.enviar_mensagem)

        # Botão para enviar mensagens
        self.botao_enviar = ctk.CTkButton(self, text="Enviar", fg_color='#111111', command=self.enviar_mensagem)
        self.botao_enviar.pack(side=tk.LEFT, padx=10, pady=10)

        # Botão para anexar arquivos
        self.botao_anexar = ctk.CTkButton(self, text="Anexar Arquivo", fg_color='#111111', command=self.anexar_arquivo)
        self.botao_anexar.pack(side=tk.RIGHT, padx=10, pady=10)


    def enviar_mensagem(self, event=None):
        mensagem = self.entrada.get()
        if mensagem.strip():
            self.area_texto.configure(state='normal')
            self.area_texto.insert(tk.END, f"Você: {mensagem}\n")
            self.area_texto.configure(state='disabled')
            self.entrada.delete(0, tk.END)
            self.area_texto.yview(tk.END)

    def anexar_arquivo(self):
        caminho_arquivo = filedialog.askopenfilename()
        if caminho_arquivo:
            nome_arquivo = os.path.basename(caminho_arquivo)
            self.area_texto.configure(state='normal')
            self.area_texto.insert(tk.END, f"{nome_arquivo} ")

            # Cria um botão para baixar o arquivo
            botao_baixar = ctk.CTkButton(self.frame_chat, text=None, command=lambda: self.baixar_arquivo(caminho_arquivo), hover=False, fg_color='white', bg_color='white', image=image_1, height=25, width=25)
            self.area_texto.window_create(tk.END, window=botao_baixar)
            self.area_texto.insert(tk.END, "\n")
            
            self.area_texto.configure(state='disabled')
            self.area_texto.yview(tk.END)

    def baixar_arquivo(self, caminho_arquivo):
        destino = filedialog.asksaveasfilename(defaultextension=".*", initialfile=os.path.basename(caminho_arquivo))
        if destino:
            with open(caminho_arquivo, 'rb') as arquivo_origem:
                with open(destino, 'wb') as arquivo_destino:
                    arquivo_destino.write(arquivo_origem.read())
            print(f"Arquivo salvo em: {destino}")


if __name__ == "__main__":
    app = ChatDosGuri()
    app.mainloop()
