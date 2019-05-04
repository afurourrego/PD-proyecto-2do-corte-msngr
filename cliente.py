from socket import *
from threading import *
from tkinter import *
import pickle
from tkinter import messagebox
import tkinter.ttk as ttk
import base64
from urllib.request import urlopen


#INITIALIZACION=================================================================

def configuracion():
    account_screen()

    global cliente_socket
    cliente_socket = socket()
    cliente_socket.connect(('localhost',9999))
    # recibir_hilo = Thread(target=recibir)
    # recibir_hilo.start()
    mainloop()

#LOGIN==========================================================================

def account_screen():
    global main_screen
    main_screen = Tk()
    width = 300
    height = 250
    screen_width = main_screen.winfo_screenwidth()
    screen_height = main_screen.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    main_screen.geometry("%dx%d+%d+%d" % (width, height, x, y))
    main_screen.resizable(0, 0)

    main_screen.title("Account Login")

    Label(main_screen, height="2").pack()
    Label(main_screen, text="El Chatsito", height="2", font=("Calibri", 13)).pack()
    Label(main_screen, text="").pack()
    Button(main_screen, text="Iniciar sesion", height="2", width="30", command = login_formulario).pack()
    Label(main_screen, text="").pack()
    Button(main_screen, text="Crear Cuenta", height="2", width="30", command = registrar_formulario).pack()

def login_formulario():
    global login_screen
    login_screen = Toplevel(main_screen)

    width = 300
    height = 250
    screen_width = login_screen.winfo_screenwidth()
    screen_height = login_screen.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    login_screen.geometry("%dx%d+%d+%d" % (width, height, x, y))
    login_screen.resizable(0, 0)

    login_screen.title("Iniciar sesion")

    global username_verify
    global password_verify
    global username_login_entry
    global password_login_entry

    username_verify = StringVar()
    password_verify = StringVar()

    Label(login_screen, height="2").pack()
    Label(login_screen, text="Nombre de Usuario * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Contraseña * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()

def login_verify():
    username_info = username_verify.get()
    password_info = password_verify.get()

    cliente_socket.send(bytes("login", "utf-8"))

    #se envia a servidor los datos para buscarlo y retorna un usuario o un error
    user_info = [username_info, password_info]
    data_string = pickle.dumps(user_info)
    cliente_socket.send(data_string)
    result = cliente_socket.recv(1024).decode("utf-8")

    if result == "exito":
        #recibe el nombre de usuario y level en una variable global
        global user_data
        user_data = cliente_socket.recv(1024)
        user_data = pickle.loads(user_data)
        main_screen.destroy()
        Home()

    else:
        login_error("Usuario y/o contraseña invalidos")

def registrar_formulario():
    global registrar_screen
    registrar_screen = Toplevel(main_screen)

    width = 300
    height = 250
    screen_width = registrar_screen.winfo_screenwidth()
    screen_height = registrar_screen.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    registrar_screen.geometry("%dx%d+%d+%d" % (width, height, x, y))
    registrar_screen.resizable(0, 0)

    registrar_screen.title("Crear Cuenta")

    global username
    global email
    global password
    global repeat_password

    global email_entry
    global username_entry
    global password_entry
    global repeat_password_entry

    username = StringVar()
    email = StringVar()
    password = StringVar()
    repeat_password = StringVar()


    Label(registrar_screen, height="1").pack()
    username_label = Label(registrar_screen, text="Nombre * ")
    username_label.pack()
    username_entry = Entry(registrar_screen, textvariable=username)
    username_entry.pack()

    email_label = Label(registrar_screen, text="Email * ")
    email_label.pack()
    email_entry = Entry(registrar_screen, textvariable=email)
    email_entry.pack()

    password_label = Label(registrar_screen, text="Contraseña *")
    password_label.pack()
    password_entry = Entry(registrar_screen, textvariable=password, show="*")
    password_entry.pack()

    repeat_password_label = Label(registrar_screen, text="Repetir Contraseña *")
    repeat_password_label.pack()
    repeat_password_entry = Entry(registrar_screen, textvariable=repeat_password, show="*")
    repeat_password_entry.pack()

    Label(registrar_screen, text="").pack()
    Button(registrar_screen, text="Crear Cuenta", width=10, height=1, command = registrar_verify).pack()

def registrar_verify():
    username_new = username.get()
    email_new = email.get()
    password_new = password.get()
    repeat_password_new = repeat_password.get()
    level = "user"

    if password_new == '' and repeat_password_new == '':
        mensajes_alerta("Debe tener contraseña", main_screen)
    elif password_new != repeat_password_new:
        mensajes_alerta("Las contraseñas deben ser iguales", main_screen)
    elif username_new == "":
        mensajes_alerta("Debe tener un nombre de usuario", main_screen)
    elif email_new == "":
        mensajes_alerta("Debe tener un email", main_screen)
    else:
        cliente_socket.send(bytes("crear_usuario", "utf-8"))
        user_new_info = [username_new, email_new, password_new, level]
        data_string = pickle.dumps(user_new_info)
        cliente_socket.send(data_string)

        registrar_screen.destroy()
        mensajes_alerta("Registro Exitoso", main_screen)


#mensajes errores login=========================================================

def login_error(mensaje):
    global login_error_screen
    mensaje_alert = StringVar()
    mensaje_alert.set(mensaje)
    login_error_screen = Toplevel(login_screen)

    width = 200
    height = 100
    screen_width = login_error_screen.winfo_screenwidth()
    screen_height = login_error_screen.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    login_error_screen.geometry("%dx%d+%d+%d" % (width, height, x, y))
    login_error_screen.resizable(0, 0)

    login_error_screen.title("info")
    Label(login_error_screen, height="1").pack()
    Label(login_error_screen, textvariable=mensaje_alert).pack()
    Button(login_error_screen, text="OK", command=login_error_screen.destroy).pack()

#HOME===========================================================================

def Home():
    global home
    home = Tk()
    home.title("El Chatsito")

    width = 1024
    height = 520
    screen_width = home.winfo_screenwidth()
    screen_height = home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    home.resizable(0, 0)

    menubar = Menu(home)

    menu_cuenta = Menu(menubar, tearoff=0)
    menu_cuenta.add_command(label="Editar Cuenta", command=editar_cuenta_formulario)
    menu_cuenta.add_command(label="Cerrar sesion", command=cerrar_sesion)
    menu_cuenta.add_command(label="Salir", command=salir)
    menubar.add_cascade(label="Cuenta", menu=menu_cuenta)

    if user_data[1] == "administrador":
        menubar.add_command(label="Usuarios", command=manage_users)


    home.config(menu=menubar)

#menu cuenta====================================================================

def editar_cuenta_formulario():
    global editar_cuenta_screen
    editar_cuenta_screen = Toplevel(home)
    editar_cuenta_screen.title("Editar usuario")

    width = 300
    height = 250
    screen_width = home.winfo_screenwidth()
    screen_height = home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    editar_cuenta_screen.geometry("%dx%d+%d+%d" % (width, height, x, y))
    editar_cuenta_screen.resizable(0, 0)

    editar_cuenta_screen.geometry("300x250")
    editar_cuenta_screen.resizable(0, 0)

    global username
    global password
    global repeat_password
    global username_entry
    global password_entry
    global repeat_password_entry
    username = StringVar()
    password = StringVar()
    repeat_password = StringVar()

    username.set(user_data[0])

    Label(editar_cuenta_screen, height="2").pack()
    username_label = Label(editar_cuenta_screen, text="Nombre * ")
    username_label.pack()
    username_entry = Entry(editar_cuenta_screen, textvariable=username)
    username_entry.pack()

    password_label = Label(editar_cuenta_screen, text="Nueva Contraseña ")
    password_label.pack()
    password_entry = Entry(editar_cuenta_screen, textvariable=password, show="*")
    password_entry.pack()

    repeat_password_label = Label(editar_cuenta_screen, text="Repetir nueva Contraseña ")
    repeat_password_label.pack()
    repeat_password_entry = Entry(editar_cuenta_screen, textvariable=repeat_password, show="*")
    repeat_password_entry.pack()

    Label(editar_cuenta_screen, text="").pack()
    Button(editar_cuenta_screen, text="Editar usuario", width=10, height=1, command = editar_cuenta).pack()

def editar_cuenta():
    username_info = username.get()
    password_info = password.get()
    repeat_password_info = repeat_password.get()

    if password_info == repeat_password_info:
        cliente_socket.send(bytes("editar", "utf-8"))
        user_info = [username_info, password_info]
        data_string = pickle.dumps(user_info)
        #INSERT
        cliente_socket.send(data_string)

        editar_cuenta_screen.destroy()
        mensajes_alerta("Actualizacion exitosa", home)
    else:
        mensajes_alerta("La contraseña no es igual", home)

def cerrar_sesion():
    result = messagebox.askquestion('info', '¿Desea cerrar sesion?', icon="warning")
    if result == 'yes':
        user_data = ''
        home.destroy()
        account_screen()

def salir():
    result = messagebox.askquestion('info', '¿Esta seguro de salir?', icon="warning")
    if result == 'yes':
        home.destroy()
        exit()

#menu usuarios==================================================================

def manage_users():
    global users_form
    users_form = Toplevel()
    users_form.title("USUARIOS")

    width = 600
    height = 400
    screen_width = home.winfo_screenwidth()
    screen_height = home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    users_form.geometry("%dx%d+%d+%d" % (width, height, x, y))
    users_form.resizable(0, 0)
    users_formulario()

def users_formulario():
    global tree
    global SEARCH
    SEARCH = StringVar()

    users_header = Frame(users_form, width=600, bd=0, relief=SOLID)
    users_header.pack(side=TOP, fill=X)

    label_users_header = Label(users_header, text="USUARIOS", font=('arial', 18), width=600)
    label_users_header.pack(fill=X)

    users_menu_left = Frame(users_form, width=600)
    users_menu_left.pack(side=LEFT, fill=Y)

    box_users_list = Frame(users_form, width=600)
    box_users_list.pack(side=RIGHT)

    label_user_search = Label(users_menu_left, text="Buscar", font=('arial', 12))
    label_user_search.pack(side=TOP, padx=27, anchor=W)
    search = Entry(users_menu_left, textvariable=SEARCH, font=('arial', 12), width=10)
    search.pack(side=TOP, padx=30, fill=X)

    btn_search = Button(users_menu_left, text="Buscar", command= lambda: search_users("usuarios"))
    btn_search.pack(side=TOP, padx=30, pady=10, fill=X)

    btn_reset = Button(users_menu_left, text="Reset", command=reset_users)
    btn_reset.pack(side=TOP, padx=30, pady=10, fill=X)

    btn_add_new = Button(users_menu_left, text="Agregar", command=add_user_form)
    btn_add_new.pack(side=TOP, padx=30, pady=10, fill=X)

    btn_edit_new = Button(users_menu_left, text="Editar", command=edit_user_form)
    btn_edit_new.pack(side=TOP, padx=30, pady=10, fill=X)

    btn_delete = Button(users_menu_left, text="Eliminar", command= lambda: delete_users("usuario"))
    btn_delete.pack(side=TOP, padx=30, pady=10, fill=X)

    scrollbarx = Scrollbar(box_users_list, orient=HORIZONTAL)
    scrollbary = Scrollbar(box_users_list, orient=VERTICAL)

    tree = ttk.Treeview(box_users_list, columns=("Codigo", "Nombre", "Nivel"), selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)

    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)

    tree.heading('Codigo', text="Codigo",anchor=W)
    tree.heading('Nombre', text="Nombre",anchor=W)
    tree.heading('Nivel', text="Nivel",anchor=W)

    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=60)

    tree.pack()
    listar_usuarios()

def listar_usuarios():
    cliente_socket.send(bytes("listar_usuarios", "utf-8"))

    users_list = cliente_socket.recv(1024)
    users_list = pickle.loads(users_list)
    for user in users_list:
        if user[0] != 1:
            tree.insert('', 'end', values=(user))

def reset_users():
    tree.delete(*tree.get_children())
    listar_usuarios()
    SEARCH.set("")

def delete_users(filtro):
    if not tree.selection():
       print("ERROR")
    else:
        result = messagebox.askquestion("info", '¿Esta seguro de eliminar?', icon="warning")
        if result == 'yes':
            cliente_socket.send(bytes("eliminar_"+filtro, "utf-8"))

            user_select = tree.focus()
            content_user = (tree.item(user_select))
            user_values = content_user['values']

            cliente_socket.send(bytes(str(user_values[0]), "utf-8"))
            manage_users()

def add_user_form():
    global user_add_screen
    user_add_screen = Toplevel(home)
    user_add_screen.title("Formulario de Registro")

    width = 300
    height = 250
    screen_width = home.winfo_screenwidth()
    screen_height = home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    user_add_screen.geometry("%dx%d+%d+%d" % (width, height, x, y))
    user_add_screen.resizable(0, 0)

    global username
    global password
    global level
    global username_entry
    global password_entry

    username = StringVar()
    password = StringVar()
    level = StringVar()

    Label(user_add_screen, height="2").pack()
    username_label = Label(user_add_screen, text="Nombre * ")
    username_label.pack()
    username_entry = Entry(user_add_screen, textvariable=username)
    username_entry.pack()
    password_label = Label(user_add_screen, text="Contraseña * ")
    password_label.pack()
    password_entry = Entry(user_add_screen, textvariable=password, show="*")
    password_entry.pack()
    level1_entry = Radiobutton(user_add_screen, text="administrador", value="administrador", variable=level)
    level1_entry.place(x=30, y=130)
    level2_entry = Radiobutton(user_add_screen, text="inventario", value="inventario", variable=level)
    level2_entry.place(x=130, y=130)
    level3_entry = Radiobutton(user_add_screen, text="cajero", value="cajero", variable=level)
    level3_entry.place(x=210, y=130)

    Label(user_add_screen, height="4").pack()
    Button(user_add_screen, text="Crear usuario", width=10, height=1, command = add_user).pack()

def add_user():
    user_new = username.get()
    pass_new = password.get()
    level_new = level.get()

    if level_new == "":
        mensajes_alerta("Debe seleccionar un Nivel", home)
    else:
        cliente_socket.send(bytes("crear_usuario", "utf-8"))
        user_new_info = [user_new, pass_new, level_new]
        data_string = pickle.dumps(user_new_info)
        cliente_socket.send(data_string)

        user_add_screen.destroy()

        mensajes_alerta("Registro Exitoso", home)
        reset_users()

def search_users(filtro):
    if SEARCH.get() != "":
        cliente_socket.send(bytes("buscar_"+filtro, "utf-8"))
        tree.delete(*tree.get_children())
        cliente_socket.send(bytes(SEARCH.get(), "utf-8"))

        users_list = cliente_socket.recv(1024)
        users_list = pickle.loads(users_list)
        for user in users_list:
            if user[0] != 1:
                tree.insert('', 'end', values=(user))

def edit_user_form():
    if not tree.selection():
       print("ERROR")
    else:
        global editar_cuenta_screen
        editar_cuenta_screen = Toplevel(home)
        editar_cuenta_screen.title("Editar usuario")

        width = 300
        height = 250
        screen_width = home.winfo_screenwidth()
        screen_height = home.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        editar_cuenta_screen.geometry("%dx%d+%d+%d" % (width, height, x, y))
        editar_cuenta_screen.resizable(0, 0)

        global code_user
        global username
        global password
        global repeat_password
        global username_entry
        global password_entry
        global repeat_password_entry

        code_user = StringVar()
        username = StringVar()
        password = StringVar()
        repeat_password = StringVar()

        select = tree.focus()
        content_select = (tree.item(select))
        select_values = content_select['values']
        code_user.set(select_values[0])
        username.set(select_values[1])

        Label(editar_cuenta_screen, height="2").pack()
        username_label = Label(editar_cuenta_screen, text="Nombre * ")
        username_label.pack()
        username_entry = Entry(editar_cuenta_screen, textvariable=username)
        username_entry.pack()

        password_label = Label(editar_cuenta_screen, text="Nueva Contraseña ")
        password_label.pack()
        password_entry = Entry(editar_cuenta_screen, textvariable=password, show="*")
        password_entry.pack()

        repeat_password_label = Label(editar_cuenta_screen, text="Repetir nueva Contraseña ")
        repeat_password_label.pack()
        repeat_password_entry = Entry(editar_cuenta_screen, textvariable=repeat_password, show="*")
        repeat_password_entry.pack()

        Label(editar_cuenta_screen, text="").pack()
        Button(editar_cuenta_screen, text="Editar usuario", width=10, height=1, command =edit_user).pack()

def edit_user():
    code_info = code_user.get()
    username_info = username.get()
    password_info = password.get()
    repeat_password_info = repeat_password.get()

    if password_info == repeat_password_info:
        cliente_socket.send(bytes("editar_usuario", "utf-8"))

        user_info = [code_info, username_info, password_info]
        data_string = pickle.dumps(user_info)
        #INSERT
        cliente_socket.send(data_string)

        editar_cuenta_screen.destroy()
        mensajes_alerta("Actualizacion exitosa", home)
        reset_users()
    else:
        mensajes_alerta("La contraseña no es igual", home)

#menu inventario================================================================


#funciones generales============================================================

def Search(filtro):
    if SEARCH.get() != "":
        cliente_socket.send(bytes("buscar_"+filtro, "utf-8"))
        tree.delete(*tree.get_children())
        cliente_socket.send(bytes(SEARCH.get(), "utf-8"))

        list = cliente_socket.recv(1024)
        list = pickle.loads(list)
        for item in list:
            if item[0] != 1:
                tree.insert('', 'end', values=(item))

#alert info=====================================================================

def mensajes_alerta(mensaje, father):
    global mensaje_alerta_screen
    mensaje_alert = StringVar()
    mensaje_alert.set(mensaje)

    mensaje_alerta_screen = Toplevel(father)
    mensaje_alerta_screen.title("info")

    width = 200
    height = 100
    screen_width = father.winfo_screenwidth()
    screen_height = father.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    mensaje_alerta_screen.geometry("%dx%d+%d+%d" % (width, height, x, y))
    mensaje_alerta_screen.resizable(0, 0)

    Label(mensaje_alerta_screen, height="1").pack()
    Label(mensaje_alerta_screen, textvariable=mensaje_alert).pack()
    Button(mensaje_alerta_screen, text="OK", command=mensaje_alerta_screen.destroy).pack()

#===============================================================================
if __name__ == "__main__":
    configuracion()
