import mysql.connector

global nombre_db, cursor
nombre_db = ''

def CREATE_DB():
    global nombre_db
    nombre_db = 'python_super_market'
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="")
    cursor = conexion.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS "+nombre_db)

def CREATE_TABLES():
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INT AUTO_INCREMENT PRIMARY KEY, name_user VARCHAR(255), password VARCHAR(255), level ENUM('administrador', 'inventario', 'cajero'))")
    cursor.execute("CREATE TABLE IF NOT EXISTS clientes (id INT AUTO_INCREMENT PRIMARY KEY, name_client VARCHAR(255), code VARCHAR(255))")
    cursor.execute("CREATE TABLE IF NOT EXISTS productos (id INT AUTO_INCREMENT PRIMARY KEY, image_url VARCHAR(255), name_product VARCHAR(255), price INT(10), stock INT(3))")
    cursor.execute("CREATE TABLE IF NOT EXISTS ventas (id INT AUTO_INCREMENT PRIMARY KEY, date TIMESTAMP, nombre_product VARCHAR(255), cantidad INT(3), price INT(10), name_user VARCHAR(255))")
    cursor.execute("CREATE TABLE IF NOT EXISTS caja (id INT AUTO_INCREMENT PRIMARY KEY, date TIMESTAMP, saldo INT(10))")

    cursor.execute("SELECT * FROM usuarios WHERE id = 1 AND level = 'administrador'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO usuarios (name_user, password, level) VALUES('admin', 'admin', 'administrador')")

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

def CREATE_USER(new_user, new_pass, new_level):
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("INSERT INTO usuarios (name_user, password, level) VALUES('"+new_user+"', '"+new_pass+"', '"+new_level+"')")

    conexion.commit()
    conexion.close()

def UPDATE_USER(user_code, user_name, user_pass):
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("UPDATE usuarios SET name_user = '"+user_name+"', password = '"+user_pass+"' WHERE id = "+user_code)

    conexion.commit()
    conexion.close()


def SELECT_PRODUCTOS():
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos")
    result = cursor.fetchall()

    conexion.commit()
    conexion.close()

    return result

def SELECT_PRODUCTOS_FILTER(filtro):
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos WHERE name_product LIKE '%"+filtro+"%'")

    result = cursor.fetchall()

    conexion.commit()
    conexion.close()

    return result

def DELETE_PRODUCTO(code):
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productos WHERE id = "+code)

    conexion.commit()
    conexion.close()

def CREATE_PRODUCTO(new_image, new_producto, new_precio, new_stock):
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("INSERT INTO productos (image_url, name_product, price, stock) VALUES('"+new_image+"', '"+new_producto+"', '"+new_precio+"', '"+new_stock+"')")

    conexion.commit()
    conexion.close()

def UPDATE_PRODUCTO(producto_code, producto_image, producto_name, producto_price, producto_stock):
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("UPDATE productos SET image_url = '"+producto_image+"', name_product = '"+producto_name+"', price = '"+producto_price+"', stock = '"+producto_stock+"' WHERE id = '"+producto_code+"'")

    conexion.commit()
    conexion.close()


def SELECT_CLIENTES():
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM clientes")
    result = cursor.fetchall()

    conexion.commit()
    conexion.close()

    return result

def SELECT_CLIENTES_FILTER(filtro):
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM clientes WHERE name_client LIKE '%"+filtro+"%' OR code LIKE '%"+filtro+"%'")

    result = cursor.fetchall()

    conexion.commit()
    conexion.close()

    return result

def DELETE_CLIENTE(code):
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM clientes WHERE id = "+code)

    conexion.commit()
    conexion.close()

def CREATE_CLIENTE(new_client, new_code):
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("INSERT INTO clientes (name_client, code) VALUES('"+new_client+"', '"+new_code+"')")

    conexion.commit()
    conexion.close()

def UPDATE_CLIENTE(id_client, edit_client, edit_code):
    conexion = mysql.connector.connect( host="localhost", user="root", passwd="", database=nombre_db)
    cursor = conexion.cursor()

    cursor.execute("UPDATE clientes SET name_client = '"+edit_client+"', code = '"+edit_code+"' WHERE id = '"+id_client+"'")

    conexion.commit()
    conexion.close()
