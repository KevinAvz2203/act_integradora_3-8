from abc import ABC, abstractmethod
from typing import List


# --- Patrón Comportamiento: Observer ---
class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass


class Subscriber(Observer):
    def __init__(self, name: str):
        self.name = name

    def update(self, message: str):
        print(f"[{self.name} recibió] {message}")


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

    def notify(self, message: str):
        for obs in self._instance._subscribers:
            obs.update(message)
