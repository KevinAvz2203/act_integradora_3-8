from notification import NotificationFactory, TimestampDecorator
from observer import Subscriber, NotificationManager
from gui import NotificationGUI
from admin_gui import AdminGUI
import threading

usuarios_activos = {}


def crear_usuario(nombre, tipo, destino):
    manager = NotificationManager()

    def on_send(mensaje, prioridad):
        notification = NotificationFactory.create_notification(tipo, destino, mensaje)
        notification = TimestampDecorator(notification)
        for sub in manager._instance._subscribers:
            if sub.name == nombre:
                sender = sub
                break
        else:
            sender = None
        if sender:
            manager.notify((notification.get_content(), prioridad), sender=sender)

    gui = NotificationGUI(f"Terminal de {nombre}", on_send)
    usuario = Subscriber(nombre, gui)
    manager.subscribe(usuario)
    usuarios_activos[nombre] = (usuario, gui)
    gui.run()
    # Cuando la ventana se cierra, elimina el usuario
    del usuarios_activos[nombre]
    manager._instance._subscribers.remove(usuario)


def agregar_usuario(nombre, tipo, destino):
    hilo = threading.Thread(
        target=crear_usuario, args=(nombre, tipo, destino), daemon=True
    )
    hilo.start()


def eliminar_usuario(nombre):
    if nombre in usuarios_activos:
        usuario, gui = usuarios_activos[nombre]
        gui.root.destroy()  # Cierra la ventana
        # El usuario será eliminado de la lista en crear_usuario al cerrar la ventana


def renombrar_usuario(old_name, new_name):
    if old_name in usuarios_activos and new_name not in usuarios_activos:
        usuario, gui = usuarios_activos[old_name]
        usuario.name = new_name
        gui.root.title(f"Terminal de {new_name}")
        usuarios_activos[new_name] = usuarios_activos.pop(old_name)


def obtener_nombres_usuarios():
    return list(usuarios_activos.keys())


def main():
    # Crea dos usuarios con sus propias ventanas
    # usuarios = [
    #     ("The Doctor", "sms", "+95475949"),
    #     ("Clara Oswald", "email", "TheOncomingStorm@gallifrey.com"),
    #     ("River Song", "push", "River's Tablet"),
    # ]
    # hilos = []
    # for nombre, tipo, destino in usuarios:
    #     hilo = threading.Thread(target=crear_usuario, args=(nombre, tipo, destino))
    #     hilo.start()
    #     hilos.append(hilo)
    # for hilo in hilos:
    #     hilo.join()

    admin = AdminGUI(
        agregar_usuario,
        eliminar_usuario,
        renombrar_usuario,
        obtener_nombres_usuarios,
    )
    admin.run()


if __name__ == "__main__":
    main()
