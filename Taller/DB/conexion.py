import pyodbc
import os
from DB import consultasDB
from login import Loggin
from animacion import cargando
import globales

def conectar(server_name):
    try:
        connection_string = "DRIVER={{SQL Server}};SERVER={};DATABASE=COPPEX;Trusted_Connection=yes;".format(server_name)
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        #cargando.anima().iniciar_animacion(globales.load)
        os.system("cls")        
        print("\nConexión exitosa a la base de datos\n")
        cursor.close()
        connection.close()
        #cargando.anima().iniciar_animacion(globales.acce)
        os.system("cls")
        Loggin()
    except pyodbc.Error as e:
        os.system("cls")
        print("Error al conectar a la base de datos:")
        print(e)
        cargando.anima().iniciar_animacion(globales.redig)
        os.system("cls")



"""

def conectar(server_name, username, password):
    try:
        # Cadena de conexión actualizada con usuario y contraseña específicos
        connection_string = "DRIVER={{SQL Server}};SERVER={};DATABASE=COPPEX;UID={};PWD={};".format(server_name, username, password)
        
        # Establecer la conexión
        connection = pyodbc.connect(connection_string)
        
        # Crear un cursor y ejecutar una consulta simple
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        
        # Animación y limpieza de pantalla (si se usa)
        # cargando.anima().iniciar_animacion(globales.load)
        os.system("cls")        
        print("\nConexión exitosa a la base de datos\n")
        
        # Cerrar cursor y conexión
        cursor.close()
        connection.close()
        
        # Animación adicional y llamada a la función de login
        # cargando.anima().iniciar_animacion(globales.acce)
        os.system("cls")
        Loggin()
    
    except pyodbc.Error as e:
        os.system("cls")
        print("Error al conectar a la base de datos:")
        print(e)
        cargando.anima().iniciar_animacion(globales.redig)
        os.system("cls")


"""