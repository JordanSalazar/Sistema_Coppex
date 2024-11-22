import os
import time
from DB import consultasDB
from menu_pricipal import main_menu
import globales

os.system("cls")

class Loggin:

    def __init__(self):
        self.Usuario = None        
        self.password = None
        self.intento = 0
        self.menu_loggin()

    def menu_loggin(self):
        while self.intento < 3:
            globales.bienvenido()
            self.correo_user = input("\nIngrese su nombre de Correo de usuario: \n")
            self.password = input("\nIngrese su Password: \n")

            if self.correo_user == "" or self.password == "":
                os.system("cls")
                print("\nEl nombre de usuario o contraseña no pueden estar vacíos.")
                self.intento += 1
                time.sleep(5)
                os.system("cls")
            else:
                user_correcto = consultasDB.buscar_usuario(self.correo_user)
                pass_correcta = consultasDB.buscar_contrasena(self.correo_user, self.password)

                if user_correcto is None or pass_correcta is None:
                    os.system("cls")
                    print(f"\nEl nombre de usuario o contraseña son incorrectos\nintentos {self.intento + 1} de 3")
                    self.intento += 1
                    time.sleep(2)
                    os.system("cls")
                else:
                    print("\nAcceso concedido.")
                    time.sleep(3)
                    os.system("cls")
                    main_menu()
                    break

        if self.intento == 3:
            globales.sin_intentos()
            exit()


