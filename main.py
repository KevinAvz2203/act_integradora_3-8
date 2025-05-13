from notification import NotificationFactory, TimestampDecorator
from observer import Subscriber, NotificationManager


def main():
    manager = NotificationManager()

    # Crear y suscribir observadores
    the_doctor = Subscriber("The Doctor")
    clara_oswald = Subscriber("Clara Oswald")
    manager.subscribe(the_doctor)
    manager.subscribe(clara_oswald)

    # Crear notificaciones
    notification1 = NotificationFactory.create_notification(
        "email",
        "TheOncomingStorm@gallifrey.com",
        "Doctor, There are Cybermen and Daleks on the loose!",
    )
    notification2 = NotificationFactory.create_notification(
        "sms", "+95475949", "Clara, I need your help! Meet me at the TARDIS."
    )

    # Decorar con timestamp
    notification1 = TimestampDecorator(notification1)
    notification2 = TimestampDecorator(notification2)

    # Notificar a todos
    manager.notify(notification1.get_content())
    manager.notify(notification2.get_content())


if __name__ == "__main__":
    main()
