import time
import os

server_name = None # o "NOMBRE_DEL_SERVIDOR_SQL"
database_name = "COPPEX"
# Credenciales de usuario
username = "TU_NOMBRE_DE_USUARIO"
password = "TU_CONTRASEÑA"
# Mensajes para animaciones o estados de carga
load = "Comprobando"
acce = "Ingresando"
redig = "Regresando"

nombre = "ICE GRASS TEA"
descripcion = "Solucion liquida"
precio_uni = 1000
fecha_vencimiento = "2025-10-10"
id_categoria = 2
cantidad = 200

cat1 = "INSERT INTO Categoria (Tipo) VALUES ('Liquido')"
cat2 = "INSERT INTO Categoria (Tipo) VALUES ('Polvo')"
cat3 = "INSERT INTO Categoria (Tipo) VALUES ('Capsula')"

def base_encontrada():
    os.system("cls")
    print("""
---------------------------------------------
Base de datos encontrada. Iniciando sesión...
---------------------------------------------          
""")
    time.sleep(4)
    os.system("cls")

def base_no_encontrada():
    os.system("cls")
    print("""
-----------------------------------------------------
Base de datos no encontrada. Iniciando instalación...
-----------------------------------------------------          
""")
    time.sleep(4)
    os.system("cls")

def base_error():
    os.system("cls")
    print("""
------------------------------------
Error al verificar la base de datos.
------------------------------------         
""")
    time.sleep(4)
    os.system("cls")

def salir():
    print("""
------------------------------------
    SALIENDO DEL SISTEMA COPPEX
------------------------------------               
""")

def error():
    print("""
-----------------------------------
    INSERTE UN VALOR VALIDO
-----------------------------------               
""")

def proceso():
    print("""
----------------------------------------
    PROCESO DE INICIO PLAT. COPPEX
----------------------------------------               
""")
    
def sin_intentos():
    print("""
-----------------------------------------------
Se han utilizado todos los intentos disponibles
Intentelo más tarde
-----------------------------------------------
    """)

def bienvenido():
    print("""
----------------------------------
  Bienvenido al Sistema COPPEX
Por favor ingrese sus credenciales
----------------------------------
    """)

def main_menu():
    print("""
----------------------------
Bienvenido al Sistema COPPEX
----------------------------

Que desea hacer?
            
    1.- Menú de cliente
    2.- Menú de Productos
    3.- Menú de Guias de despacho
    4.- Menú de Facturas

    5.- Salir                            
                        """)
    

def cliente_opt():
    print("""
----------------------------------
            CLIENTES
----------------------------------
          
Que desea hacer?
            
    1.- Ingresar Cliente
    2.- Visualizar Clientes
    3.- Modificar Clientes

    4.- Salir   
    """)

def cliente_ing():
    print("""
----------------------------------
        INGRESAR CLIENTES
---------------------------------- 
    """)

def cliente_ing_clear():
    print("""
----------------------------------
   CLIENTE INGRESADO CON EXITO
---------------------------------- 
    """)

def vis_clientes():
    print("""
Que desea hacer?
          
1.- Modificar Cliente
2.- Salir
""")
    
def nuestrosClientes():
    print("""
----------------------------------
        NUESTROS CLIENTES
---------------------------------- 
""")
    
def modificarCliente():
    print("""
----------------------------------
        MODIFICAR CLIENTE
----------------------------------
""")
    

def menuproductos():
    print("""
----------------------------------
            PRODUCTOS
----------------------------------
          
Que desea hacer?
            
    1.- Ingresar Productos
    2.- Visualizar Productos
    3.- Modificar Productos

    4.- Salir   
    """)

def ingresar_producto():
    print("""
----------------------------------
        INGRESAR PRODUCTO
----------------------------------
          
Para ingresar un producto necesita los siguientes datos:  
    """)

def producto_ing_clear():
    print("""
----------------------------------
   PRODUCTO INGRESADO CON EXITO
---------------------------------- 
    """)

def nuestrosProductos():
    print("""
----------------------------------
        NUESTROS PRODUCTOS
---------------------------------- 
""")

def vis_productos():
    print("""
Que desea hacer?
          
1.- Modificar Productos
2.- Salir
""")

# ------- PESTAÑA GUIAS DE DESPACHO ------- 
def guias_despacho():
    print("""
----------------------------------
        GUIAS DE DESPACHO
---------------------------------- 
""")
    
def menu_guia():
    print("""
Que desea hacer?
          
1.- Crear Guia de Despacho
2.- Buscar guia
3.- Salir
""")
    
def crear_guias_des():
    print("""
----------------------------------
     CREAR GUIAS DE DESPACHO
---------------------------------- 
""")
    
def datos_guias():
    print("""
Ingrese los datos de la guia (ID Cliente/Direccion de envio/Fecha emisión )
""")
    
def datos_producto():
    print("""
Ingrese los datos del Producto (ID Producto/Cantidad)
""")

def buscar_g():
    print("""
----------------------------------
    BUSCAR GUIAS DE DESPACHO
---------------------------------- 
""")
    
def vis_guias():
    print("""
Que desea hacer?
          
1.- Ver detalle guia
2.- Salir
""")

def vis_guias_det():
    print("""
Que desea hacer?

1.- Salir
""")
# ----------------------------------------- 

# ------- PESTAÑA GUIAS DE DESPACHO ------- 
# ----------------------------------------- 
def facturas():
    print("""
----------------------------------
        NUESTRAS FACTURAS
---------------------------------- 
""")
    
def menu_factura():
    print("""
Que desea hacer?
          
1.- Crear Factura
2.- Buscar Factura
3.- Salir
""")
    
def crear_factura():
    print("""
----------------------------------
           CREAR FACTURA
---------------------------------- 
""")
    
def datos_factura():
    print("""
Ingrese los datos para generar la Factura (ID Despacho/Fecha de emisión/Estado de pago)
""")

def vis_factura():
    print("""
Que desea hacer?
          
1.- Modificar Factura
2.- Salir
""") 
    
def modFactura():
    print("""
----------------------------------
        MODIFICAR FACTURA
---------------------------------- 
""")
# -----------------------------------------