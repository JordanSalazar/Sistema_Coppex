import pestanas
import globales
import os
import time

import pestanas.clientes
import pestanas.factura
import pestanas.guia_despacho
import pestanas.productos

def opcion_menu(opcion):

    os.system("cls")

    if opcion == '1': # Clientes
        pestanas.clientes.menu_cliente()
    elif opcion == '2': # Productos
        pestanas.productos.Productos()
    elif opcion == '3': # Guias de despacho
        pestanas.guia_despacho.guias()
    elif opcion == '4': # Facturas
        pestanas.factura.facturacion()
    elif opcion == '5': # Salir
        globales.salir()
        time.sleep(5)
        exit()
    else:
        os.system("cls")
        globales.error()
        time.sleep(3)



    
