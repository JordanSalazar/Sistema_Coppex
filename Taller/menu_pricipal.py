import os
import option_menu
import globales

class main_menu():
    def __init__(self):
        self.option = None
        self.menu_principal()

    def menu_principal(self):
        while True:
            try:
                os.system("cls")
                globales.main_menu()
                self.opcion = input("ingrese valor: ")
                option_menu.opcion_menu(self.opcion)

            except ValueError:
                print(ValueError)

