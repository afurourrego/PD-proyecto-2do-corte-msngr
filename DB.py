import mysql.connector

global nombre_db, cursor
nombre_db = ''

def CREATE_DB():
    global nombre_db
    nombre_db = 'python_chat_msngr'
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="")
    cursor = conexion.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS "+nombre_db)

def CREATE_TABLES():
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INT AUTO_INCREMENT PRIMARY KEY, name_user VARCHAR(255), email VARCHAR(255), password VARCHAR(255), level ENUM('administrador', 'user'))")

    cursor.execute("SELECT * FROM usuarios WHERE id = 1 AND level = 'administrador'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO usuarios (name_user, email, password, level) VALUES('admin', 'admin@admin.com', '123', 'administrador')")

    conexion.commit()
    conexion.close()

def SEARCH_USER_LOGIN(user_name, user_pass):
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE name_user = '"+user_name+"' AND password = '"+user_pass+"'")
    result = cursor.fetchone()

    conexion.commit()
    conexion.close()

    return result

def UPDATE_CUENTA(user_code, user_name, user_pass):
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("UPDATE usuarios SET name_user = '"+user_name+"', password = '"+user_pass+"' WHERE id = "+str(user_code))

    conexion.commit()
    conexion.close()

def SELECT_USERS():
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("SELECT id, name_user, level FROM usuarios")
    result = cursor.fetchall()

    conexion.commit()
    conexion.close()

    return result

def SELECT_USERS_FILTER(filtro):
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("SELECT id, name_user, level FROM usuarios WHERE name_user LIKE '%"+filtro+"%' OR level LIKE '%"+filtro+"%'")

    result = cursor.fetchall()

    conexion.commit()
    conexion.close()

    return result

def DELETE_USER(code):
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id = "+code)

    conexion.commit()
    conexion.close()

def CREATE_USER(new_user, new_email, new_pass, new_level):
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("INSERT INTO usuarios (name_user, email, password, level) VALUES('"+new_user+"', '"+new_email+"', '"+new_pass+"', '"+new_level+"')")

    conexion.commit()
    conexion.close()

def UPDATE_USER(user_code, user_name, user_pass):
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("UPDATE usuarios SET name_user = '"+user_name+"', password = '"+user_pass+"' WHERE id = "+user_code)

    conexion.commit()
    conexion.close()
