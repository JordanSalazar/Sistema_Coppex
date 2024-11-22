import pyodbc
import os
import login
from DB import conexion_test
from DB import consultasDB
import globales

class instalar():

    def __init__(self):
        self.comprobar_server = int
        self.comprobar_base = int
        self.opcion = None
        self.compr_server()

    def compr_server(self):
        self.comprobar_server = conexion_test.conectar_base()

        if self.comprobar_server == 0:
            self.compr_base()
        elif self.comprobar_server == 2:
            print("Servidor no encontrado.")
        elif self.comprobar_server == 3:
            print("Error al conectar con el servidor.")

    def compr_base(self):
        self.comprobar_base = conexion_test.verificar_base_datos()

        if self.comprobar_base == 0:
            globales.base_encontrada()
            login.Loggin()
        elif self.comprobar_base == 2:
            globales.base_no_encontrada()
            self.instalar()
        elif self.comprobar_base == 3:
            globales.base_error()


    def instalar(self):
        conexion_test.instalar()
        conexion_test.instalar_proce()
        consultasDB.agregar_admin()
        login.Loggin()