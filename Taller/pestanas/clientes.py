import os
import globales
import time
import menu_pricipal
from DB import consultasDB

os.system("cls")

class menu_cliente():
    def __init__(self):
        self.opcion = None
        self.opciones()

    def opciones(self):
        while True:
            try:
                os.system("cls")
                globales.cliente_opt()
                self.opcion = input("ingrese valor: ")

                if self.opcion == '1': # Ingresar Cliente
                    self.ingresar_cliente()

                elif self.opcion == '2': # Visualizar Clientes
                    os.system("cls")
                    globales.nuestrosClientes()
                    consultasDB.mostrar_cliente()
                    self.visualizar_clientes()

                elif self.opcion == '3': # Modificar Clientes
                    self.modificar_cliente()

                elif self.opcion == '4': # Regresar a menu principal
                    menu_pricipal.main_menu()

                else:
                    os.system("cls")
                    globales.error()
                    time.sleep(3)

            except ValueError:
                    os.system("cls")
                    globales.error()
                    time.sleep(3)
    
    def ingresar_cliente(self):
        os.system("cls")
        globales.cliente_ing()
        print("""
-----------------------------------------------------------------------
Ingrese los datos solicitados o ingrese 0 en cualquier campo para salir
-----------------------------------------------------------------------
    """)
        
        def obtener_input(mensaje, max_caracteres):
            entrada = input(mensaje)
            if entrada == "0":
                self.opciones()
                return None
            while len(entrada) > max_caracteres:
                print(f"\nEl valor ingresado supera los {max_caracteres} caracteres permitidos. Intente nuevamente.")
                entrada = input(mensaje)
                if entrada == "0":
                    self.opciones()
                    return None
            return entrada
        
        rut = obtener_input("\nIngrese Rut del Cliente o 0 para salir: (Maximo 10 caracteres, sin puntos ni guión)\n", 10)
        if rut is None: return
        razon = obtener_input("\nIngrese Razon Social del Cliente: (Maximo 100 Caracteres)\n", 100)
        if razon is None: return
        giro = obtener_input("\nIngrese Giro del Cliente: (Maximo 100 caracteres)\n", 100)
        if giro is None: return
        correo = obtener_input("\nIngrese Correo del Cliente: (Maximo 50 caracteres)\n", 50)
        if correo is None: return
        telefono = obtener_input("\nIngrese Telefono del Cliente: (Maximo 12 caracteres)\n", 12)
        if telefono is None: return
        consultasDB.agregar_usuario(rut,razon, giro, correo, telefono)
        os.system("cls")
        print("""
-----------------------------------------------------------------------
        Los datos ingresados se han almacenado correctamente
-----------------------------------------------------------------------
    """)
        time.sleep(4)
        self.opciones()

    def visualizar_clientes(self):
        while True:
            try:
                os.system("cls")
                globales.nuestrosClientes()
                consultasDB.mostrar_cliente()
                globales.vis_clientes()
                self.opcion = input("Ingrese su opcion:\n")
                if self.opcion == "1":
                    self.modificar_cliente()
                elif self.opcion == "2":
                    self.opciones()

                else:
                    os.system("cls")
                    globales.error()
                    time.sleep(3)

            except ValueError:
                    os.system("cls")
                    globales.error()
                    time.sleep(3)

    def modificar_cliente(self):
        os.system("cls")
        globales.nuestrosClientes()
        consultasDB.mostrar_cliente()
        print("""
--------------------------------------------
Ingrese el ID Cliente o escriba 0 para salir
--------------------------------------------
    """)
        while True:
            try:
                cliente = input("Ingrese un valor (máximo 6 caracteres):\n")

                if cliente.isdigit(): # isdigit() es un metodo que verifica si el valor ingresado es entero
                    if len(cliente) > 6:
                        print("Error: El ID del Cliente no debe superar los 6 caracteres.")
                        time.sleep(4)
                        self.opciones()
                    else:
                        cliente_id = int(cliente)

                        if cliente_id != 0:
                            self.modificacion(cliente_id)
                        elif cliente == "0":
                            os.system("cls")
                            self.opciones()
                            break
                else:
                    os.system("cls")
                    print("Ingrese una opcion valida")
                    time.sleep(3)
                    self.visualizar_clientes()
            except ValueError:
                os.system("cls")
                globales.error()
                time.sleep(3)
    
    def modificacion(self, cliente_id):
        os.system("cls")
        globales.modificarCliente()
        consultasDB.mostrar_un_cliente(cliente_id)
        
        atributos_validos = {
            "Rut": 10,
            "Razon_social": 100,
            "Giro": 100,
            "Correo": 50,
            "Telefono": 12,
            "Fecha_baja":None
        }
        
        try:
            atributo = input("\nIngrese el nombre del atributo que desea modificar (Rut, Razon_social, Giro, Correo, Telefono, Fecha_baja): \n")
            
            if atributo not in atributos_validos:
                print("\nAtributo no válido.")
                time.sleep(3)
                self.modificacion(cliente_id)
                return
            
            limite = atributos_validos[atributo]
            valor = input("\nIngrese el nuevo valor para el atributo: \n")
            
            if limite is not None and len(valor) > limite:
                print(f"\nEl valor ingresado supera los {limite} caracteres permitidos para {atributo}.")
                time.sleep(3)
                self.modificacion(cliente_id)
                return
            
            if atributo == "Telefono":
                valor = int(valor)
            
            consultasDB.actualizar_atributo_cliente(cliente_id, atributo, valor)
            os.system("cls")
            print(f"""
--------------------------------------------------------------------------------                  
    Cliente con ID {cliente_id} ha sido actualizado, {atributo} cambiado a {valor}.
--------------------------------------------------------------------------------""")
            time.sleep(3)
            
            volver = input("\nDesea modificar otro valor? (si/no):\n").strip().lower()
            if volver == "si":
                self.modificacion(cliente_id)
            elif volver == "no":
                self.opciones()
            else:
                print("\nOpción no válida.")
                time.sleep(3)
                self.opciones()
        
        except ValueError:
            print("\nError en los valores ingresados.")
            time.sleep(3)
            self.modificacion(cliente_id)
