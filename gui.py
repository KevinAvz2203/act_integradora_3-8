import tkinter as tk
from tkinter import scrolledtext


class NotificationGUI:
    def __init__(self, title, on_send_callback):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.configure(bg="black")
        self.on_send_callback = on_send_callback

        self.text_area = scrolledtext.ScrolledText(
            self.root, width=80, height=20, bg="black", fg="lime", font=("Courier", 12)
        )
        self.text_area.pack(padx=10, pady=10)
        self.text_area.config(state=tk.DISABLED)

        self.priority_var = tk.StringVar(value="Media")
        self.priority_menu = tk.OptionMenu(
            self.root, self.priority_var, "Alta", "Media", "Baja"
        )
        self.priority_menu.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))

        self.entry = tk.Entry(self.root, width=50, font=("Courier", 12))
        self.entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))

        self.send_button = tk.Button(
            self.root, text="Enviar", command=self.send_message
        )
        self.send_button.pack(side=tk.LEFT, padx=(5, 10), pady=(0, 10))

    def show_notification(self, message, priority="Media"):
        color = {"Alta": "red", "Media": "yellow", "Baja": "lime"}.get(priority, "lime")
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, message + "\n", priority)
        self.text_area.tag_config(priority, foreground=color)
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)

    def send_message(self):
        message = self.entry.get()
        priority = self.priority_var.get()
        if message.strip():
            self.on_send_callback(message, priority)
            self.entry.delete(0, tk.END)

    def run(self):
        self.root.mainloop()
