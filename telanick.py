import customtkinter as ctk
from tkinter import messagebox

def entrar(event=None):
    global nickname_entry, root
    nickname = nickname_entry.get()
    if nickname:  
        print(f'Nickname inserido: {nickname}')
        root.nickname = nickname  # Define o atributo nickname no root para acessá-lo posteriormente
        root.destroy()  # Fecha a janela
    else:
        messagebox.showwarning('Campo vazio', 'Campo de nickname vazio. Por favor, insira um nickname.')

root = ctk.CTk()
root.geometry('1280x720')
root.title('Chat dos guri')

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

nickname_label = ctk.CTkLabel(root, text='Insira seu nickname:', font=('Arial', 25))
nickname_label.grid(row=0, column=0, pady=(20, 5))

nickname_entry = ctk.CTkEntry(root)
nickname_entry.grid(row=1, column=0, pady=5, padx=10)
nickname_entry.bind('<Return>', entrar)

enter_button = ctk.CTkButton(root, text='Entrar', command=entrar)
enter_button.grid(row=2, column=0, pady=(5, 20))

root.mainloop()
