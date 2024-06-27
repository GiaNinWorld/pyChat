import customtkinter as ctk
from tkinter import messagebox

# inicializa o app
app = ctk.CTk()
app.geometry('1280x720')
app.title('Chat dos guri')

#func de entrar

def entrar(event=None):
    nickname = nickname_entry.get()
    if nickname:  
        print (f'Nickname inserido: {nickname}')
    else:
        messagebox.showwarning('Campo vazio', 'Campo de nickname vazio. Por favor, insira um nickname.')

#centlaizar os widgets

app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)
app.grid_columnconfigure(0, weight=1)

#entrada nickname
nickname_label = ctk.CTkLabel(app, text='Insira seu nickname:', font=('Arial', 25))
nickname_label.grid(row=0, column=0, pady=(20, 5))

nickname_entry = ctk.CTkEntry(app)
nickname_entry.grid(row=1, column=0, pady=5, padx=10)
nickname_entry.bind('<Return>', entrar)

#boatao para entrar
enter_button = ctk.CTkButton(app, text='Entre', command=entrar)
enter_button.grid(row=2, column=0, pady=(5, 20))

app.mainloop()
