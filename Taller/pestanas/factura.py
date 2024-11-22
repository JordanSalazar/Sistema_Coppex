import os
import globales
import time
import menu_pricipal
from DB import consultasDB
import datetime

class facturacion():

    def __init__(self): 
        self.opcion: None
        self.menuF()
    

    def menuF(self):
        while True:
            try:
                os.system("cls")
                globales.facturas()
                globales.menu_factura()

                self.opcion = int(input("Ingrese su opcion: \n"))

                if self.opcion == 1: # Crear Factura
                    self.crear_factura()

                elif self.opcion == 2: # Buscar Factura
                    self.buscar_factura()
                
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

    def crear_factura(self):
        os.system("cls")
        globales.crear_factura()
        globales.datos_factura()
        consultasDB.mostrar_datos_guia_despacho()

        id_despacho = int(input("\nIngrese ID de Despacho: \n"))
        estado = input("\nIngrese el estado de pago (Pagado/Pendiente/Anulado): \n")
        while True:
            fecha_emision = input("\nIngrese la fecha de despacho (YYYY-MM-DD): \n")
            try:
                fecha = datetime.datetime.strptime(fecha_emision, "%Y-%m-%d").date()
                break  # Salir del bucle si la fecha es válida
            except ValueError:
                print("Formato de fecha incorrecto. Por favor ingrese la fecha en formato YYYY-MM-DD.")
        
        consultasDB.insertar_factura(id_despacho, fecha, estado)
        self.menuF()

    def buscar_factura(self):
        while True:
            try:
                os.system("cls")
                globales.buscar_g()
                consultasDB.mostrar_facturas()
                globales.vis_factura()
                self.opcion = input("\nIngrese su opcion:\n")
                if self.opcion == "1":
                    self.modificarfactura()
                elif self.opcion == "2":
                    self.menuF()

                else:
                    os.system("cls")
                    globales.error()
                    time.sleep(3)

            except ValueError:
                    os.system("cls")
                    globales.error()
                    time.sleep(3)

    def modificarfactura(self):
        os.system("cls")
        globales.modFactura()
        consultasDB.mostrar_facturas()
        
        while True:
            factura = input("\nIngrese el ID de la factura (6 caracteres): \n")
            
            if len(factura) >= 6 or not factura.isdigit():
                print("Error: El ID de la factura no puede superar los 6 caracteres.")
                time.sleep(4)
                self.buscar_factura()
            else:
                factura = int(factura)
                break

        try:
            os.system("cls")
            globales.modFactura()
            consultasDB.buscar_factura(factura)

            estado = input("\nIngrese el estado actual de la Factura (Pagado/Pendiente/Anulado): \n").capitalize()
            
            if estado not in ["Pagado", "Pendiente", "Anulado"]:
                os.system("cls")
                globales.error()
                time.sleep(3)
                self.modificarfactura()  # Corrección en la llamada recursiva
                return
            
            else:
                consultasDB.modificarfactura(factura, estado)
                time.sleep(3)
                self.menuF()
        
        except ValueError:
            os.system("cls")
            globales.error()
            time.sleep(3)


