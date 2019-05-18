from socket import *
from threading import *
import mysql.connector

clientes = {}
direcciones = {}

def configuracion():
    global servidor
    servidor = socket()
    servidor.bind(("", 9998))
    servidor.listen(10)
    print("Esperando conexiones...")
    aceptar_hilo = Thread(target=aceptar_conexiones)
    aceptar_hilo.start()
    aceptar_hilo.join()

def aceptar_conexiones():
    while True:
        cliente_local, direccion_cliente = servidor.accept()
        print("%s:%s conectado. "% direccion_cliente)
        cliente_local.send(bytes("Bienvenido...", "utf-8"))
        direcciones[cliente_local] = direccion_cliente
        Thread(target=encargarse_cliente,args=(cliente_local,)).start()

def encargarse_cliente(cliente):
    nombre = cliente.recv(1024).decode("utf-8")
    clientes[cliente] = nombre
    while True:
        print("chat conectado")

        # if opcion =="chat_grupal":
        # cliente.send(bytes("bienvenido", "utf-8"))
        print("2")
        # while True:
        mensaje = cliente.recv(1024).decode("utf-8")
        print("3")
        # guardar_mensaje(nombre, mensaje)
        # broadcast(mensaje)
        if mensaje != "{salir}":
            # guardar_mensaje(nombre, mensaje)
            broadcast(mensaje, nombre)
        else:
            del clientes[cliente]
            broadcast(bytes("%s ha salido del chat." % nombre, "utf-8"))
            break

def broadcast(mensaje, prefix=""):
    print("enviando a todos")
    for sock in clientes:
        sock.send(bytes(prefix +": " + mensaje, "utf-8"))

# def guardar_mensaje(nombre,mensaje):
#     conexion = mysql.connector.connect(user="root", password="", host="localhost", database="chat")
#     cursor = conexion.cursor()
#     sql = "INSERT INTO comunicaciones(usuario, mensaje)VALUES(%s,%s)"
#     parametros = (str(nombre), str(mensaje))
#     cursor.execute(sql,parametros)
#     conexion.commit()
#     conexion.close


# def broadcast(mensaje, prefix=""):
#     for sock in clientes:
#         sock.send(bytes(prefix + mensaje, "utf-8"))

if __name__ == "__main__":
    configuracion()
