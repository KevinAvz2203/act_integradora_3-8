from abc import ABC, abstractmethod
from typing import List


# --- Patrón Comportamiento: Observer ---
class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass


class Subscriber(Observer):
    def __init__(self, name: str, gui=None):
        self.name = name
        self.gui = gui

    def update(self, message_with_priority):
        if isinstance(message_with_priority, tuple):
            message, priority = message_with_priority
        else:
            message, priority = message_with_priority, "Media"

        # Extrae el adjunto si existe
        adjunto = None
        if "[Adjunto:" in message:
            start = message.find("[Adjunto:") + 9
            end = message.find("]", start)
            adjunto = message[start:end].strip()
            message = message.replace(f" [Adjunto: {adjunto}]", "")

        output = f"[{self.name} recibió] {message}"
        with open("historial.txt", "a", encoding="utf-8") as f:
            f.write(output + f" [Prioridad: {priority}]\n")
        if self.gui:
            self.gui.root.after(
                0, self.gui.show_notification, output, priority, adjunto
            )
        else:
            print(output)


# --- Patrón Creacional Extra: Singleton ---
class NotificationManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NotificationManager, cls).__new__(cls)
            cls._instance._subscribers = []
        return cls._instance

    def subscribe(self, observer: Observer):
        self._instance._subscribers.append(observer)

    def notify(self, message_with_priority, sender):
        for obs in self._instance._subscribers:
            if obs != sender:
                obs.update(message_with_priority)
