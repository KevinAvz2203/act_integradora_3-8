import os
import shutil
import winsound

from PIL import Image, ImageTk
from tkinter import scrolledtext, filedialog
import tkinter as tk


class NotificationGUI:
    def __init__(self, title, on_send_callback, master=None):
        if master is None:
            self.root = tk.Tk()
        else:
            self.root = tk.Toplevel(master)
        self.root.title(title)

        self.root.configure(bg="black")
        self.on_send_callback = on_send_callback
        self.attachment_path = None
        self.image_refs = []

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

        self.entry = tk.Entry(self.root, width=40, font=("Courier", 12))
        self.entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))

        self.attach_button = tk.Button(
            self.root, text="Adjuntar archivo", command=self.attach_file
        )
        self.attach_button.pack(side=tk.LEFT, padx=(5, 0), pady=(0, 10))

        self.send_button = tk.Button(
            self.root, text="Enviar", command=self.send_message
        )
        self.send_button.pack(side=tk.LEFT, padx=(5, 10), pady=(0, 10))

        self.attachment_frame = tk.Frame(self.root, bg="black")
        self.attachment_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

    def attach_file(self):
        """
        Opens a file dialog to select a file and copies it to the 'images' directory.
        Updates the attachment button to indicate a file is attached.
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            os.makedirs("images", exist_ok=True)
            filename = os.path.basename(file_path)
            dest_path = os.path.join("images", filename)

            if not os.path.exists(dest_path):
                shutil.copy(file_path, dest_path)
            self.attachment_path = filename
            self.attach_button.config(text="Archivo adjunto")

    def show_notification(self, message, priority="Media", adjunto=None):
        """
        Displays a notification message in the chat window, with color based on priority.
        If an attachment is provided, displays an image or file label accordingly.

        Args:
            message (str): The notification message.
            priority (str): The priority level ("Alta", "Media", "Baja").
            adjunto (str, optional): The filename of the attachment.
        """
        try:
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except Exception:
            pass

        for widget in self.attachment_frame.winfo_children():
            widget.destroy()
        self.image_refs.clear()

        color = {"Alta": "red", "Media": "yellow", "Baja": "lime"}.get(priority, "lime")
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, message + "\n", priority)
        self.text_area.tag_config(priority, foreground=color)
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)

        if adjunto:
            adjunto_path = os.path.join("images", adjunto)
            if os.path.exists(adjunto_path):
                ext = os.path.splitext(adjunto_path)[1].lower()

                if ext in [".png", ".jpg", ".jpeg", ".gif"]:
                    try:
                        print("Intentando abrir:", adjunto_path)
                        img = Image.open(adjunto_path)
                        img.thumbnail((200, 200))
                        photo = ImageTk.PhotoImage(img)
                        label = tk.Label(self.attachment_frame, image=photo, bg="black")
                        label.pack(side=tk.LEFT, padx=5)
                        self.image_refs.append(photo)
                    except Exception as e:
                        label = tk.Label(
                            self.attachment_frame,
                            text=f"Imagen inválida: {adjunto}",
                            fg="white",
                            bg="black",
                        )
                        label.pack(side=tk.LEFT, padx=5)
                else:
                    label = tk.Label(
                        self.attachment_frame,
                        text=f"Archivo: {adjunto}",
                        fg="white",
                        bg="black",
                    )
                    label.pack(side=tk.LEFT, padx=5)

    def send_message(self):
        """
        Collects the message, priority, and attachment, then calls the send callback.
        Resets the entry and attachment button after sending.
        """
        message = self.entry.get()
        priority = self.priority_var.get()
        attachment = self.attachment_path
        if message.strip():
            self.on_send_callback(message, priority, attachment)
            self.entry.delete(0, tk.END)
            self.attachment_path = None
            self.attach_button.config(text="Adjuntar archivo")

    def run(self):
        self.root.mainloop()
