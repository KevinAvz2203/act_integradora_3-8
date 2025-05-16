import tkinter as tk

from admin_gui import AdminGUI
from gui import NotificationGUI
from notification import NotificationFactory, TimestampDecorator
from observer import Subscriber, NotificationManager

active_users = {}


def create_user(name, type, receiver, on_user_update, master):
    """
    Creates a new user, their GUI, and subscribes them to the NotificationManager.

    Args:
        name (str): The user's name.
        type (str): The notification type.
        receiver (str): The notification receiver.
        on_user_update (callable): Callback to update users.
        master (tk.Tk): The main Tkinter window.
    """
    manager = NotificationManager()

    def on_send(message, priority, attachment):
        """
        Sends a notification through the NotificationManager.

        Args:
            message (str): The message to send.
            priority (str): The message priority.
            attachment (str): Optional attachment.
        """
        notification = NotificationFactory.create_notification(type, receiver, message)
        notification = TimestampDecorator(notification)
        content = notification.get_content()
        if attachment:
            content += f" [Attachment: {attachment}]"
        for sub in manager._instance._subscribers:
            if sub.name == name:
                sender = sub
                break
        else:
            sender = None
        if sender:
            manager.notify((content, priority), sender=sender)

    gui = NotificationGUI(f"Terminal de {name}", on_send, master=master)
    user = Subscriber(name, gui)
    manager.subscribe(user)
    active_users[name] = (user, gui)

    gui.show_notification(
        f"Welcome to the Tardis Group Chat!, it's great seeing you here {name}!",
        "Media",
    )

    gui.run()
    del active_users[name]
    manager._instance._subscribers.remove(user)


def add_user(name, type, receiver, on_user_update):
    """
    Adds a new user to the chat.

    Args:
        name (str): The user's name.
        type (str): The notification type.
        receiver (str): The notification receiver.
        on_user_update (callable): Callback to update users.
    """
    create_user(name, type, receiver, on_user_update, root)


def delete_user(name, on_user_update=None):
    """
    Removes an active user and closes their chat window.

    Args:
        name (str): The user's name to remove.
        on_user_update (callable, optional): Callback to update users.
    """
    if name in active_users:
        user, gui = active_users[name]
        try:
            gui.root.after(0, gui.root.destroy)
        except Exception:
            pass


def rename_user(old_name, new_name):
    """
    Changes the name of an active user.

    Args:
        old_name (str): The user's current name.
        new_name (str): The user's new name.
    """
    if old_name in active_users and new_name not in active_users:
        user, gui = active_users[old_name]
        user.name = new_name
        gui.root.title(f"Chat window of {new_name}")
        active_users[new_name] = active_users.pop(old_name)


def get_users_names():
    """Returns a list of active user names."""
    return list(active_users.keys())


def main():
    global root
    root = tk.Tk()
    root.withdraw()

    admin = AdminGUI(
        add_user,
        delete_user,
        rename_user,
        get_users_names,
        master=root,
    )
    admin.run()


if __name__ == "__main__":
    main()
