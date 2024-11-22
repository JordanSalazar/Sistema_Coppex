import pyodbc
from DB import DB_install
from DB import DB_proced_install
import globales

def conectar_base():
    try:
        # Cadena de conexión utilizando Trusted Connection
        connection_string = f"DRIVER={{SQL Server}};SERVER={globales.server_name};Trusted_Connection=yes;"
        connection = pyodbc.connect(connection_string)
        
        # Crear un cursor y ejecutar una consulta simple
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        # Cerrar cursor y conexión
        cursor.close()
        connection.close()
        
        # Verificar si el servidor existe
        if result[0] is not None:
            return 0
        else:
            return 2
        
    except pyodbc.Error as e:
        print("Error al conectar al conectar con el servidor o al ejecutar la consulta:")
        print(e)
        return 3
    


""" Autenticacion usuario contraseña sql server

def conectar_base():
    try:
        # Cadena de conexión utilizando nombre de usuario y contraseña
        connection_string = (
            f"DRIVER={{SQL Server}};SERVER={globales.server_name};"
            f"UID={globales.username};PWD={globales.password};"
        )
        connection = pyodbc.connect(connection_string)
        
        # Crear un cursor y ejecutar una consulta simple
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        # Cerrar cursor y conexión
        cursor.close()
        connection.close()
        
        # Verificar si el servidor existe
        if result[0] is not None:
            return 0
        else:
            return 2
        
    except pyodbc.Error as e:
        print("Error al conectar con el servidor o al ejecutar la consulta:")
        print(e)
        return 3

"""



def verificar_base_datos():
    try:
        connection_string = f"DRIVER={{SQL Server}};SERVER={globales.server_name};Trusted_Connection=yes;"
        connection = pyodbc.connect(connection_string)
        
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sys.databases WHERE name = ?", globales.database_name)
        result = cursor.fetchone()

        cursor.close()
        connection.close()
        
        if result is not None:
            return 0  # Base de datos existe
        else:
            return 2  # Base de datos no existe
        
    except pyodbc.Error as e:
        print("Error al conectar con el servidor o al verificar la base de datos:")
        print(e)
        return 3  # Error al verificar
    
def instalar():
    try:
        # Cadena de conexión utilizando Trusted Connection
        connection_string = f"DRIVER={{SQL Server}};SERVER={globales.server_name};Trusted_Connection=yes;"
        connection = pyodbc.connect(connection_string)
        
        # Crear un cursor
        cursor = connection.cursor()
        
        # Ejecutar las consultas definidas en DB_install
        for query in [DB_install.crear, DB_install.clientes, DB_install.usuarios,
                      DB_install.categoria, DB_install.productos, DB_install.inventario,
                      DB_install.guia, DB_install.despacho, DB_install.detalle, DB_install.factura]:
            cursor.execute(query)
            connection.commit()

        # Cerrar cursor y conexión
        cursor.close()
        connection.close()
        
    except pyodbc.Error as e:
        print("Error al conectar a la base de datos o al ejecutar la consulta:")
        print(e)

def instalar_proce():
    try:
        # Cadena de conexión utilizando Trusted Connection
        connection = pyodbc.connect("DRIVER={{SQL server}}; SERVER={}; DATABASE=COPPEX; Trusted_Connection=yes;".format(globales.server_name))

        # Crear un cursor
        cursor = connection.cursor()
        
        # Lista de procedimientos almacenados a instalar
        procedures = [
            DB_proced_install.act_atrib_client,
            DB_proced_install.crear_tabla,
            DB_proced_install.insert_product,
            DB_proced_install.act_product,
            DB_proced_install.vis_inv_prod,
            DB_proced_install.bus_prod_id,
            DB_proced_install.insert_guia,
            DB_proced_install.mostrar_guia,
            DB_proced_install.mostrar_detal,
            DB_proced_install.inser_fact,
            DB_proced_install.modif_fact,
            DB_proced_install.selec_fact
        ]

        # Ejecutar cada consulta de procedimiento almacenado
        for sql in procedures:
            try:
                cursor.execute(sql)
                connection.commit()
            except pyodbc.Error as e:
                print(f"Error al ejecutar la consulta:\n{sql}")
                print(e)
        
        # Cerrar cursor y conexión
        cursor.close()
        connection.close()
        
    except pyodbc.Error as e:
        print("Error al conectar a la base de datos o al ejecutar la consulta:")
        print(e)



