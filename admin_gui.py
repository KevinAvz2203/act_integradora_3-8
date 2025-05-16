import tkinter as tk


class AdminGUI:
    def __init__(self, on_add_user, on_remove_user, on_rename_user, get_users):
        self.root = tk.Tk()
        self.root.title("Administrar Usuarios")
        self.on_add_user = on_add_user
        self.on_remove_user = on_remove_user
        self.on_rename_user = on_rename_user
        self.get_users = get_users

        tk.Label(self.root, text="Nombre:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Tipo:").grid(row=1, column=0)
        self.type_var = tk.StringVar(value="sms")
        self.type_menu = tk.OptionMenu(self.root, self.type_var, "sms", "email", "push")
        self.type_menu.grid(row=1, column=1)

        tk.Label(self.root, text="Destino:").grid(row=2, column=0)
        self.dest_entry = tk.Entry(self.root)
        self.dest_entry.grid(row=2, column=1)

        self.add_button = tk.Button(
            self.root, text="Agregar Usuario", command=self.add_user
        )
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Lista de usuarios
        self.users_listbox = tk.Listbox(self.root)
        self.users_listbox.grid(row=4, column=0, columnspan=2, pady=10)
        self.refresh_users()

        self.remove_button = tk.Button(
            self.root, text="Eliminar Usuario", command=self.remove_user
        )
        self.remove_button.grid(row=5, column=0, pady=5)

        self.rename_entry = tk.Entry(self.root)
        self.rename_entry.grid(row=5, column=1, pady=5)
        self.rename_button = tk.Button(
            self.root, text="Renombrar Usuario", command=self.rename_user
        )
        self.rename_button.grid(row=6, column=0, columnspan=2, pady=5)

    def refresh_users(self):
        self.users_listbox.delete(0, tk.END)
        for user in self.get_users():
            self.users_listbox.insert(tk.END, user)

    def add_user(self):
        nombre = self.name_entry.get()
        tipo = self.type_var.get()
        destino = self.dest_entry.get()
        if nombre and tipo and destino:
            self.on_add_user(nombre, tipo, destino)
            self.name_entry.delete(0, tk.END)
            self.dest_entry.delete(0, tk.END)
            self.refresh_users()

    def remove_user(self):
        selection = self.users_listbox.curselection()
        if selection:
            nombre = self.users_listbox.get(selection[0])
            self.on_remove_user(nombre)
            self.refresh_users()

    def rename_user(self):
        selection = self.users_listbox.curselection()
        new_name = self.rename_entry.get()
        if selection and new_name:
            old_name = self.users_listbox.get(selection[0])
            self.on_rename_user(old_name, new_name)
            self.rename_entry.delete(0, tk.END)
            self.refresh_users()

    def run(self):
        self.root.mainloop()
