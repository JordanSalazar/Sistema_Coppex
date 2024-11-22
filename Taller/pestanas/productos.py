import os
import globales
import time
import menu_pricipal
from DB import consultasDB
import datetime


class Productos():
    def __init__(self):
        self.opcion: None
        self.menuP()
    
    def menuP(self):
        while True:
            try:
                os.system("cls")
                globales.menuproductos()
                self.opcion = int(input("Ingrese su opcion:\n"))

                if self.opcion == 1: # Ingresar Productos
                    self.ingresar_productos()

                elif self.opcion == 2: # Visualizar Productos
                    self.visualizar_productos()
                
                elif self.opcion == 3: # Modificar Productos
                    self.modificar_productos()

                elif self.opcion == 4: # Salir
                    menu_pricipal.main_menu()

                else:
                    os.system("cls")
                    globales.error()
                    time.sleep(3)

            except ValueError:
                    os.system("cls")
                    globales.error()
                    time.sleep(3)

    def ingresar_productos(self):
        os.system("cls")
        globales.ingresar_producto()

        nombre = input("\nIngrese el nombre del producto: \n")
        descripcion = input("\nIngrese la descripción del producto: \n")
        precio_uni = int(input("\nIngrese el precio unitario del producto: (sin puntos ni '$')\n"))
        while True:
            fecha_venc = input("\nIngrese la fecha de vencimiento (YYYY-MM-DD): \n")
            try:
                fecha_vencimiento = datetime.datetime.strptime(fecha_venc, "%Y-%m-%d").date()
                break  # Salir del bucle si la fecha es válida
            except ValueError:
                print("\nFormato de fecha incorrecto. Por favor ingrese la fecha en formato YYYY-MM-DD.")

        id_categoria = int(input("\nIngrese la categoria del producto (1-Liquido, 2-Polvo, 3-Capsula): \n"))
        cantidad = int(input("\nIngrese el stock disponible (sin puntos “.” ni comas “,”): \n"))

        os.system("cls")
        consultasDB.insertar_producto(nombre,descripcion,precio_uni,fecha_vencimiento,id_categoria,cantidad)
        self.menuP()

    def visualizar_productos(self):
        while True:
            try:
                os.system("cls")
                globales.nuestrosProductos()
                consultasDB.mostrar_productos()
                globales.vis_productos()
                self.opcion = input("Ingrese su opcion:\n")
                if self.opcion == "1":
                    self.modificar_productos()
                elif self.opcion == "2":
                    self.menuP()

                else:
                    os.system("cls")
                    globales.error()
                    time.sleep(3)

            except ValueError:
                    os.system("cls")
                    globales.error()
                    time.sleep(3)

    def modificar_productos(self):
        os.system("cls")
        globales.nuestrosProductos()
        consultasDB.mostrar_productos()
        print("""
--------------------------------------------
Ingrese el ID Producto o escriba 0 para salir
--------------------------------------------
    """)
        while True:
            try:
                producto = input("Ingrese el ID Producto:\n")

                if producto.isdigit(): # isdigit() es un metodo que verifica si el valor ingresado es entero
                    if len(producto) > 6:
                        print("Error: Ha excedido el limite de caracteres.")
                        time.sleep(4)
                        self.visualizar_productos()
                    else:
                        producto_id = int(producto)

                        if producto_id != 0:
                            self.modificacion(producto_id)
                        elif producto == "0":
                            os.system("cls")
                            self.menuP()
                            break
                else:
                    os.system("cls")
                    globales.error()
                    time.sleep(3)
                    self.modificar_productos()
            except ValueError:
                os.system("cls")
                globales.error()
                time.sleep(3)

    def modificacion(self, producto_id):
        os.system("cls")
        globales.nuestrosProductos()
        consultasDB.buscar_producto_por_id(producto_id)
        
        try:
            atributo = input("\nIngrese el nombre del atributo que desea modificar (Nombre, Descripcion, Precio_uni, fecha_vencimiento, Stock): \n")
            
            if atributo not in ["Nombre", "Descripcion", "Precio_uni", "fecha_vencimiento", "Stock"]:
                print("Atributo no válido.")
                time.sleep(3)
                self.menuP()
                return
            
            valor = input("\nIngrese el nuevo valor para el atributo: \n")
            if atributo == "Telefono":
                valor = int(valor)
            
            consultasDB.actualizar_producto(producto_id, atributo, valor)
            print(f"\Producto con ID {producto_id} ha sido actualizado, {atributo} cambiado a {valor}.\n")
            time.sleep(3)
            
            volver = input("Desea modificar otro valor? (si/no):\n").strip().lower()
            if volver == "si":
                self.modificacion(producto_id)
            elif volver == "no":
                self.menuP()
            else:
                print("Opción no válida.")
                time.sleep(3)
                self.menuP()
        
        except ValueError:
            print("Error en los valores ingresados.")
            time.sleep(3)
            self.modificacion(producto_id)