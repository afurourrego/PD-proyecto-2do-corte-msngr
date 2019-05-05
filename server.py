from socket import *
from threading import *
import pickle
import DB

clientes = {}
direcciones = {}
DB.CREATE_DB()
DB.CREATE_TABLES()


def configuracion():
    global servidor
    servidor = socket()
    servidor.bind(("", 9999))
    servidor.listen(10)
    print("Esperando conexiones...")
    aceptar_hilo = Thread(target=aceptar_conexiones)
    aceptar_hilo.start()
    aceptar_hilo.join()

def aceptar_conexiones():
    while True:
        cliente_local, direccion_cliente = servidor.accept()
        print("%s:%s conectado. "% direccion_cliente)
        direcciones[cliente_local] = direccion_cliente
        Thread(target=encargarse_cliente,args=(cliente_local,)).start()

def encargarse_cliente(cliente):
    while True:
        opcion = cliente.recv(1024).decode("utf-8")

        #================================LOGIN
        if opcion == 'login':
            print("login")
            user_info =  cliente.recv(1024)
            user_info = pickle.loads(user_info)
            result = DB.SEARCH_USER_LOGIN(user_info[0], user_info[1])

            if result is None:
                cliente.send(bytes("error", "utf-8"))
            else:
                cliente.send(bytes("exito", "utf-8"))
                #envia el nombre de usuario y level
                user_logged = [result[0], result[1], result[2], result[3], result[4]]
                result = [result[1], result[4], result[2]]
                data_string = pickle.dumps(result)
                cliente.send(data_string)
                clientes[cliente] = user_logged[1]

        if opcion == 'editar':
            print("editar")
            user_edit =  cliente.recv(1024)
            user_edit = pickle.loads(user_edit)
            if user_edit[2] == '':
                DB.UPDATE_CUENTA(user_logged[0], user_edit[0], user_edit[1], user_logged[3])
            else:
                DB.UPDATE_CUENTA(user_logged[0], user_edit[0], user_edit[1], user_edit[2])
                user_logged[2] = user_edit[1]
            user_logged[1] = user_edit[0]

        #================================USUARIOS
        if opcion == "listar_usuarios":
            print("listar usuarios")
            result = DB.SELECT_USERS()
            data_string = pickle.dumps(result)
            cliente.send(data_string)

        if opcion == "buscar_usuarios":
            print("buscar usuarios")
            filtro = cliente.recv(1024).decode("utf-8")
            result = DB.SELECT_USERS_FILTER(filtro)
            data_string = pickle.dumps(result)
            cliente.send(data_string)

        if opcion == "eliminar_usuario":
            print("eliminar usuario")
            user_code = cliente.recv(1024).decode("utf-8")
            DB.DELETE_USER(user_code)

        if opcion == "crear_usuario":
            print("crear usuario")
            user_new =  cliente.recv(1024)
            user_new = pickle.loads(user_new)
            print(user_new)
            DB.CREATE_USER(user_new[0], user_new[1], user_new[2], user_new[3])

        if opcion == 'editar_usuario':
            print("editar usuario")
            user_edit =  cliente.recv(1024)
            user_edit = pickle.loads(user_edit)
            DB.UPDATE_USER(user_edit[0], user_edit[1], user_edit[2])

        #================================HOME

        if opcion == "listar_usuarios_online":
            print("listar usuarios online")
            result = DB.SELECT_USERS_ONLINE()
            data_string = pickle.dumps(result)
            cliente.send(data_string)

        #=================================MENSAJES

        if opcion == "mensaje_grupal":
            print("mensaje grupal")
            mensaje = cliente.recv(1024)
            # guardar_mensaje(nombre, mensaje)
            broadcast(mensaje, user_logged[1]+": ")

def broadcast(mensaje, prefix=""):
    for sock in clientes:
        sock.send(bytes(prefix, "utf-8")+mensaje)

# def guardar_mensaje(nombre,mensaje):
#     conexion = mysql.connector.connect(user="root", password="", host="localhost", database="chat")
#     cursor = conexion.cursor()
#     sql = "INSERT INTO comunicaciones(usuario, mensaje)VALUES(%s,%s)"
#     parametros = (str(nombre), str(mensaje))
#     cursor.execute(sql,parametros)
#     conexion.commit()
#     conexion.close

if __name__ == "__main__":
    configuracion()
