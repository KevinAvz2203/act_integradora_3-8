from abc import ABC, abstractmethod
import datetime


# --- Patrón Creacional: Factory Method ---
class Notification(ABC):
    @abstractmethod
    def get_content(self) -> str:
        pass


class EmailNotification(Notification):
    def __init__(self, recipient: str, text: str):
        self.recipient = recipient
        self.text = text

    def get_content(self) -> str:
        return f"Email to {self.recipient}: {self.text}"


class SMSNotification(Notification):
    def __init__(self, phone: str, text: str):
        self.phone = phone
        self.text = text

    def get_content(self) -> str:
        return f"SMS to {self.phone}: {self.text}"


class PushNotification(Notification):
    def __init__(self, device: str, text: str):
        self.device = device
        self.text = text

    def get_content(self) -> str:
        return f"Push to {self.device}: {self.text}"


class NotificationFactory:
    @staticmethod
    def create_notification(kind: str, target: str, text: str) -> Notification:
        if kind == "email":
            return EmailNotification(target, text)
        elif kind == "sms":
            return SMSNotification(target, text)
        elif kind == "push":
            return PushNotification(target, text)
        else:
            raise ValueError("The Tardis doesn't have this kind on its database.")


# --- Patrón Estructural: Decorator ---
class NotificationDecorator(Notification):
    def __init__(self, wrapped: Notification):
        self._wrapped = wrapped

    @abstractmethod
    def get_content(self) -> str:
        pass


class TimestampDecorator(NotificationDecorator):
    def get_content(self) -> str:
        original = self._wrapped.get_content()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{now}] {original}"
