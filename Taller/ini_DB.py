import os
import time
import globales
import instalacion
from DB import conexion
from DB import conexion_test
os.system("cls")

class dataini:
    
    def __init__(self):
        self.nombre_data = None
        self.intentos = 0
        self.iniciar()

    def iniciar(self):
        while self.intentos < 3:
            globales.proceso()
            globales.server_name = input("\nIngrese Server name: ")
            
            if globales.server_name == "":
                os.system("cls")
                print("nDebe ingresar el nombre del servidor")
                self.intentos += 1
                time.sleep(2)
                os.system("cls")
            else:
                os.system("cls")
                instalacion.instalar()

        if self.intentos == 3:
            globales.sin_intentos()
            exit()
        

