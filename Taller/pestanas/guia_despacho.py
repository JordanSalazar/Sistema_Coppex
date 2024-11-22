import os
import globales
import time
import menu_pricipal
from DB import consultasDB
import datetime

class guias():

    def __init__(self): 
        self.opcion: None
        self.menuG()
    

    def menuG(self):
        while True:
            try:
                os.system("cls")
                globales.guias_despacho()
                globales.menu_guia()

                self.opcion = int(input("\nIngrese su opcion: \n"))

                if self.opcion == 1: # Crear Guia de Despacho
                    self.crear_guia()

                elif self.opcion == 2: # Buscar guia de despacho
                    self.buscar_guia()
                
                elif self.opcion == 3: # Salir
                    menu_pricipal.main_menu()

                else:
                    os.system("cls")
                    globales.error()
                    time.sleep(3)

            except ValueError:
                    os.system("cls")
                    globales.error()
                    time.sleep(3)


    def crear_guia(self):
        os.system("cls")
        globales.crear_guias_des()
        globales.datos_guias()
        consultasDB.mostrar_cliente()

        id_cliente = int(input("\nIngrese ID del cliente o 0 para salir: \n"))
        
        if id_cliente == 0:
            self.menuG()

        else:
            direccion = input("\nIngrese la dirección de envío: \n")
            while True:
                fecha_emision = input("\nIngrese la fecha de despacho (YYYY-MM-DD): \n")
                try:
                    fecha = datetime.datetime.strptime(fecha_emision, "%Y-%m-%d").date()
                    break  # Salir del bucle si la fecha es válida
                except ValueError:
                    print("\nFormato de fecha incorrecto. Por favor ingrese la fecha en formato YYYY-MM-DD.")
            
            self.insertar_productos(fecha, direccion, id_cliente)

    def insertar_productos(self, fecha, direccion, id_cliente):
        os.system("cls")
        globales.crear_guias_des()
        globales.datos_producto()
        consultasDB.mostrar_productos()

        productos = []

        while True:
            id_producto = int(input("\nIngrese ID del Producto: \n"))
            cantidad = int(input("\nIngrese la cantidad: \n"))
            productos.append({'ID_Producto': id_producto, 'Cantidad': cantidad})
            
            continuar = input("\n¿Desea agregar otro producto? (s/n): \n")
            if continuar.lower() != 's':
                break

        consultasDB.insertar_guia_y_productos_despacho(fecha, direccion, id_cliente, productos)
        time.sleep(15)
        self.menuG()

    def buscar_guia(self):
        while True:
            try:
                os.system("cls")
                globales.buscar_g()
                consultasDB.mostrar_datos_guia_despacho()
                globales.vis_guias()
                self.opcion = input("\nIngrese su opcion:\n")
                
                if self.opcion == "1":
                    while True:
                        id_guia = input("\nIngrese el ID de la Guia: \n")
                        
                        if len(id_guia) > 6 or not id_guia.isdigit():
                            print("\nError: El ID de la Guia no puede superar los 6 caracteres numéricos.")
                            time.sleep(4)
                            self.menuG()
                        else:
                            id_guia = int(id_guia)
                            break
                    
                    self.mostrar_detalle(id_guia)
                elif self.opcion == "2":
                    self.menuG()
                else:
                    os.system("cls")
                    globales.error()
                    time.sleep(3)

            except ValueError:
                os.system("cls")
                globales.error()
                time.sleep(3)

    def mostrar_detalle(self,id_guia):
        while True:
            try:
                os.system("cls")
                globales.buscar_g()
                consultasDB.detalle_completo(id_guia)
                globales.vis_guias_det()
                self.opcion = input("\nIngrese su opcion:\n")
                if self.opcion == "1":
                    self.menuG()

                else:
                    os.system("cls")
                    globales.error()
                    time.sleep(3)

            except ValueError:
                    os.system("cls")
                    globales.error()
                    time.sleep(3)
