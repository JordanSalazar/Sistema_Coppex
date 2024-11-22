import pyodbc
import globales
import time
import datetime
from pestanas import clientes
from pestanas import factura
from pestanas import productos


# //----- INSERTAR USUARIO TEMPORTAL y PRODUCTO -----//
def agregar_admin():
    connection = pyodbc.connect("DRIVER={{SQL server}}; SERVER={}; DATABASE=COPPEX; Trusted_Connection=yes;".format(globales.server_name))
    cursor = connection.cursor() 
    sql = "INSERT INTO Usuarios (Cargo, Nombre, Apellido, Email, Pass) VALUES ('Admin','COPPEX', 'None', 'admin@example.com', 'admin123')"
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
    insertar_categoria()

def insertar_categoria():
    # Configurar la conexión a la base de datos
    connection = pyodbc.connect("DRIVER={{SQL Server}}; SERVER={}; DATABASE=COPPEX; Trusted_Connection=yes;".format(globales.server_name))
    cursor = connection.cursor()
 
    # Crear un cursor
    cursor = connection.cursor()
    
    # Ejecutar las consultas definidas en DB_install
    for query in [globales.cat1, globales.cat2, globales.cat3]:
        cursor.execute(query)
        connection.commit()

    # Cerrar cursor y conexión
    cursor.close()
    connection.close()
    insertar_producto_base()

def insertar_producto_base():
    # Configurar la conexión a la base de datos
    connection = pyodbc.connect("DRIVER={{SQL Server}}; SERVER={}; DATABASE=COPPEX; Trusted_Connection=yes;".format(globales.server_name))
    cursor = connection.cursor()

    try:
        # Construir la consulta SQL de forma segura
        sql = f"""
        EXEC InsertarProducto 
            @Nombre = '{globales.nombre}', 
            @Descripcion = '{globales.descripcion}', 
            @Precio_Uni = {globales.precio_uni}, 
            @Fecha_vencimiento = '{globales.fecha_vencimiento}', 
            @ID_Categoria = {globales.id_categoria}, 
            @Cantidad = {globales.cantidad}
        """
        cursor.execute(sql)
        
        # Confirmar los cambios
        connection.commit()
    
    except Exception as e:
        print("Error al insertar el producto:", e)
        time.sleep(10)
        import traceback
        print(traceback.format_exc())
        time.sleep(10)
        connection.rollback()  # Deshacer cambios en caso de error
    
    finally:
        # Cerrar cursor y conexión
        cursor.close()
        connection.close()


# //--------------------------------------//

# //----- CONSULTA LOGIN -----//
def buscar_usuario(correo_user):
    connection = pyodbc.connect("DRIVER={{SQL server}}; SERVER={}; DATABASE=COPPEX; Trusted_Connection=yes;".format(globales.server_name))
    cursor = connection.cursor() 
    sql = "SELECT Email FROM Usuarios WHERE Email = '{}'".format(correo_user)
    cursor.execute(sql)
    resultado = cursor.fetchone()
    return resultado

def buscar_contrasena(correo_user, password):
    connection = pyodbc.connect("DRIVER={{SQL server}}; SERVER={}; DATABASE=COPPEX; Trusted_Connection=yes;".format(globales.server_name))
    cursor = connection.cursor() 
    sql = "SELECT Pass FROM Usuarios WHERE Email = '{}' and Pass = '{}'".format(correo_user, password)
    cursor.execute(sql)
    resultado = cursor.fetchone()
    return resultado
# //----------------------------//


# //----- AGREGAR CLIENTES -----//
def agregar_usuario(rut,razon, giro, correo, telefono):
   connection = pyodbc.connect("DRIVER={{SQL server}}; SERVER={}; DATABASE=COPPEX; Trusted_Connection=yes;".format(globales.server_name))
   cursor = connection.cursor() 
   sql = "INSERT INTO Clientes (Rut, Razon_social, Giro, Correo, Telefono) VALUES ('{}','{}', '{}', '{}', '{}')".format(rut,razon, giro, correo, telefono)
   cursor.execute(sql)
   connection.commit()
   cursor.close()
# //----------------------------//

# //-------------------------------FUNCIONES CLIENTE---------------------------------------------//
# //----- MOSTRAR TODOS LOS CLIENTES -----//
def mostrar_cliente():
    connection = pyodbc.connect("DRIVER={{SQL server}}; SERVER={}; DATABASE=COPPEX; Trusted_Connection=yes;".format(globales.server_name))
    cursor = connection.cursor()
    sql = "SELECT * FROM Clientes"
    cursor.execute(sql)
    
    # Obtener nombres de las columnas
    columnas = [desc[0] for desc in cursor.description]
    
    # Obtener todos los resultados
    resultados = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    # Calcular el ancho máximo para cada columna
    anchos = [len(col) for col in columnas]
    for fila in resultados:
        for i, valor in enumerate(fila):
            anchos[i] = max(anchos[i], len(str(valor)))
    
    # Crear un formato de cadena para cada fila
    formato = ' | '.join([f'{{:<{anchos[i]}}}' for i in range(len(anchos))])
    
    # Imprimir nombres de las columnas
    print(formato.format(*columnas))
    print('-' * (sum(anchos) + 3 * (len(anchos) - 1)))  # Línea separadora
    
    # Imprimir resultados
    for fila in resultados:
        print(formato.format(*map(str, fila)))
    
    return columnas, resultados
# //--------------------------------------//


# //----- MOSTRAR UN CLIENTE -----//
def mostrar_un_cliente(id_cliente):
    connection = pyodbc.connect("DRIVER={{SQL server}}; SERVER={}; DATABASE=COPPEX; Trusted_Connection=yes;".format(globales.server_name))
    cursor = connection.cursor()
    sql = "SELECT * FROM Clientes WHERE ID_Cliente = ?"
    cursor.execute(sql, id_cliente)
    
    # Obtener nombres de las columnas
    columnas = [desc[0] for desc in cursor.description]
    
    # Obtener el resultado
    resultado = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if resultado:
        # Calcular el ancho máximo para cada columna
        anchos = [len(col) for col in columnas]
        for i, valor in enumerate(resultado):
            anchos[i] = max(anchos[i], len(str(valor)))
        
        # Crear un formato de cadena para la fila
        formato = ' | '.join([f'{{:<{anchos[i]}}}' for i in range(len(anchos))])
        
        # Imprimir nombres de las columnas
        print(formato.format(*columnas))
        print('-' * (sum(anchos) + 3 * (len(anchos) - 1)))  # Línea separadora
        
        # Imprimir el resultado
        print(formato.format(*map(str, resultado)))
    else:
        print(f"No se encontró un cliente con ID {id_cliente}")
        time.sleep(4)
        clientes.menu_cliente()

    
    return columnas, resultado
# //------------------------------//


# //----- MODIFICAR CLIENTES -----//
def actualizar_atributo_cliente(id_cliente, atributo, valor):
    connection = pyodbc.connect("DRIVER={{SQL server}}; SERVER={}; DATABASE=COPPEX; Trusted_Connection=yes;".format(globales.server_name))
    cursor = connection.cursor()
    
    # Llamar al procedimiento almacenado
    sql = """EXEC ActualizarAtributoCliente @ID_Cliente=?, @Atributo=?, @Valor=?"""
    cursor.execute(sql, id_cliente, atributo, valor)
    
    connection.commit()  # Confirmar los cambios
    cursor.close()
    connection.close()
# //------------------------------//
# //---------------------------------------------------------------------------------------------//


# //-------------------------------FUNCIONES PRODUCTOS--------------------------------------------//
# //----- INSERTAR PRODUCTOS -----//
def insertar_producto(nombre, descripcion, precio_uni, fecha_vencimiento, id_categoria, cantidad):
    # Configurar la conexión a la base de datos
    connection = pyodbc.connect("DRIVER={{SQL Server}}; SERVER={}; DATABASE=COPPEX; Trusted_Connection=yes;".format(globales.server_name))
    cursor = connection.cursor()

    try:
        # Construir la consulta SQL de forma segura
        sql = f"""
        EXEC InsertarProducto 
            @Nombre = '{nombre}', 
            @Descripcion = '{descripcion}', 
            @Precio_Uni = {precio_uni}, 
            @Fecha_vencimiento = '{fecha_vencimiento}', 
            @ID_Categoria = {id_categoria}, 
            @Cantidad = {cantidad}
        """
        cursor.execute(sql)
        
        # Confirmar los cambios
        connection.commit()
        print(f"Producto '{nombre}' insertado correctamente.")
    
    except Exception as e:
        print("Error al insertar el producto:", e)
        time.sleep(10)
        import traceback
        print(traceback.format_exc())
        time.sleep(10)
        connection.rollback()  # Deshacer cambios en caso de error
    
    finally:
        # Cerrar cursor y conexión
        cursor.close()
        connection.close()

# //------------------------------//

# //----- MOSTRAR TODOS LOS PRODUCTOS -----//
def mostrar_productos():
    connection = pyodbc.connect("DRIVER={{SQL server}}; SERVER={}; DATABASE=COPPEX; Trusted_Connection=yes;".format(globales.server_name))
    cursor = connection.cursor()
    sql = "EXEC VisualizarInventarioProductos"
    cursor.execute(sql)
    
    # Obtener nombres de las columnas
    columnas = [desc[0] for desc in cursor.description]
    
    # Obtener todos los resultados
    resultados = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    # Calcular el ancho máximo para cada columna
    anchos = [len(col) for col in columnas]
    for fila in resultados:
        for i, valor in enumerate(fila):
            anchos[i] = max(anchos[i], len(str(valor)))
    
    # Crear un formato de cadena para cada fila
    formato = ' | '.join([f'{{:<{anchos[i]}}}' for i in range(len(anchos))])
    
    # Imprimir nombres de las columnas
    print(formato.format(*columnas))
    print('-' * (sum(anchos) + 3 * (len(anchos) - 1)))  # Línea separadora
    
    # Imprimir resultados
    for fila in resultados:
        print(formato.format(*map(str, fila)))
    
    return columnas, resultados
# //----------------------------------------//

# //----- MOSTRAR TODOS LOS PRODUCTOS -----//
def buscar_producto_por_id(id_producto):
    connection = pyodbc.connect("DRIVER={{SQL Server}};SERVER={};DATABASE=COPPEX;Trusted_Connection=yes;".format(globales.server_name))
    cursor = connection.cursor()
    
    try:
        # Construir la consulta SQL
        sql = "EXEC BuscarProductoPorID @ID_Producto = ?"
        cursor.execute(sql, id_producto)
        
        # Obtener nombres de las columnas
        columnas = [desc[0] for desc in cursor.description]
        
        # Obtener el resultado
        resultado = cursor.fetchone()
        
        if resultado:
            # Calcular el ancho máximo para cada columna
            anchos = [len(col) for col in columnas]
            for i, valor in enumerate(resultado):
                anchos[i] = max(anchos[i], len(str(valor)))
            
            # Crear un formato de cadena para la fila
            formato = ' | '.join([f'{{:<{anchos[i]}}}' for i in range(len(anchos))])
            
            # Imprimir nombres de las columnas
            print(formato.format(*columnas))
            print('-' * (sum(anchos) + 3 * (len(anchos) - 1)))  # Línea separadora
            
            # Imprimir el resultado
            print(formato.format(*map(str, resultado)))
        else:
            print(f"No se encontró un producto con ID {id_producto}")
            time.sleep(4)
            productos.Productos()
    
    except Exception as e:
        print("Error al buscar el producto:", e)
        import traceback
        print(traceback.format_exc())
    
    finally:
        # Cerrar cursor y conexión
        cursor.close()
        connection.close()
# //----------------------------------------//

# //----- ACTUALIZAR PRODUCTOS -----//
def actualizar_producto(id_producto, atributo, nuevo_valor):
    # Configurar la conexión a la base de datos
    connection_string = "DRIVER={{SQL Server}};SERVER={};DATABASE=COPPEX;Trusted_Connection=yes;".format(globales.server_name)
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    try:
        # Construir la consulta SQL como una cadena formateada
        if isinstance(nuevo_valor, str):
            nuevo_valor_formateado = f"'{nuevo_valor}'"
        else:
            nuevo_valor_formateado = nuevo_valor

        sql = f"""
        EXEC ActualizarProducto 
            @ID_Producto = {id_producto}, 
            @Atributo = '{atributo}', 
            @Nuevo_Valor = {nuevo_valor_formateado}
        """
        cursor.execute(sql)
        
        # Confirmar los cambios
        connection.commit()
        print(f"Atributo '{atributo}' del producto con ID '{id_producto}' actualizado correctamente.")
    
    except Exception as e:
        print("Error al actualizar el producto:", e)
        time.sleep(10)
        import traceback
        print(traceback.format_exc())
        time.sleep(10)
        connection.rollback()  # Deshacer cambios en caso de error
    
    finally:
        # Cerrar cursor y conexión
        cursor.close()
        connection.close()
# //--------------------------------//
# //----------------------------------------------------------------------------------------------//

# //----------------------------FUNCIONES GUIAS DESPACHO------------------------------------------//
# //----- CREAR GUIA DE DESPACHO Y ALMACENAR PRODUCTO -----//
def insertar_guia_y_productos_despacho(fecha_emision, direccion, id_cliente, productos):
    # Configurar la conexión a la base de datos
    connection = pyodbc.connect("DRIVER={{SQL Server}}; SERVER={}; DATABASE=COPPEX; Trusted_Connection=yes;".format(globales.server_name))
    cursor = connection.cursor()

    try:
        # Verificar si el tipo de tabla TipoProductoCantidad existe antes de crearlo
        cursor.execute("SELECT * FROM sys.types WHERE name = 'TipoProductoCantidad';")
        if not cursor.fetchone():  # Si no se encuentra el tipo, entonces crearlo
            cursor.execute("""
                CREATE TYPE TipoProductoCantidad AS TABLE
                (
                    ID_Producto INT,
                    Cantidad INT
                );
            """)

        # Crear una tabla temporal en SQL Server para almacenar los productos
        cursor.execute("CREATE TABLE #TempProductos (ID_Producto INT, Cantidad INT);")
        
        # Insertar los productos en la tabla temporal
        for producto in productos:
            cursor.execute("INSERT INTO #TempProductos (ID_Producto, Cantidad) VALUES (?, ?);",
                           int(producto['ID_Producto']), int(producto['Cantidad']))
        
        # Ejecutar el procedimiento almacenado con la tabla temporal como parámetro
        cursor.execute(f"""
            DECLARE @productosTipo TipoProductoCantidad;
            INSERT INTO @productosTipo (ID_Producto, Cantidad)
            SELECT ID_Producto, Cantidad FROM #TempProductos;

            EXEC sp_InsertarGuiaYProductosDespacho 
                @Fecha_emision = '{fecha_emision}',
                @Direccion = '{direccion}',
                @ID_Cliente = {id_cliente},
                @Productos = @productosTipo;
        """)
        # Eliminar la tabla temporal después de usarla
        cursor.execute("DROP TABLE #TempProductos;")
        
        # Confirmar los cambios
        connection.commit()

    except pyodbc.Error as e:
        print("Error al insertar la guía y los productos en el despacho:", e)
        import traceback
        print(traceback.format_exc())
        connection.rollback()  # Deshacer cambios en caso de error

    finally:
        # Cerrar cursor y conexión
        cursor.close()
        connection.close()
# //-------------------------------------------------------//

# //----- MOSTRAR TODAS LAS GUIAS DE DESPACHO -----//
def mostrar_datos_guia_despacho():
    try:
        # Establecer la conexión a la base de datos
        connection_string = "DRIVER={{SQL Server}};SERVER={};DATABASE=COPPEX;Trusted_Connection=yes;".format(globales.server_name)
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Ejecutar el procedimiento almacenado
        cursor.execute("EXEC sp_MostrarDatosGuiaDespacho;")

        # Obtener nombres de las columnas
        columnas = [desc[0] for desc in cursor.description]

        # Obtener todos los resultados
        resultados = cursor.fetchall()

        # Calcular el ancho máximo para cada columna
        anchos = [len(col) for col in columnas]
        for fila in resultados:
            for i, valor in enumerate(fila):
                anchos[i] = max(anchos[i], len(str(valor)))

        # Crear un formato de cadena para cada fila
        formato = ' | '.join([f'{{:<{anchos[i]}}}' for i in range(len(anchos))])

        # Imprimir nombres de las columnas
        print(formato.format(*columnas))
        print('-' * (sum(anchos) + 3 * (len(anchos) - 1)))  # Línea separadora

        # Imprimir resultados
        for fila in resultados:
            print(formato.format(*map(str, fila)))

    except pyodbc.Error as e:
        print(f"Error al mostrar los datos de la guía de despacho: {e}")

    finally:
        # Cerrar cursor y conexión
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
# //-----------------------------------------------//

# //----- MOSTRAR TODAS LAS GUIAS DE DESPACHO -----//
def detalle_completo(id_despacho):
    try:
        # Establecer la conexión a la base de datos
        connection_string = "DRIVER={{SQL Server}};SERVER={};DATABASE=COPPEX;Trusted_Connection=yes;".format(globales.server_name)
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Ejecutar el procedimiento almacenado con parámetro
        cursor.execute("EXEC sp_MostrarDetalleDespachoCompleto @ID_Despacho = ?;", id_despacho)

        # Obtener nombres de las columnas
        columnas = [desc[0] for desc in cursor.description]

        # Obtener todos los resultados
        resultados = cursor.fetchall()

        # Calcular el ancho máximo para cada columna
        anchos = [len(col) for col in columnas]
        for fila in resultados:
            for i, valor in enumerate(fila):
                anchos[i] = max(anchos[i], len(str(valor)))

        # Crear un formato de cadena para cada fila
        formato = ' | '.join([f'{{:<{anchos[i]}}}' for i in range(len(anchos))])

        # Imprimir nombres de las columnas
        print(formato.format(*columnas))
        print('-' * (sum(anchos) + 3 * (len(anchos) - 1)))  # Línea separadora

        # Imprimir resultados
        for fila in resultados:
            print(formato.format(*map(str, fila)))

    except pyodbc.Error as e:
        print(f"Error al mostrar el detalle completo del despacho: {e}")

    finally:
        # Cerrar cursor y conexión
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
# //-----------------------------------------------//
# //----------------------------------------------------------------------------------------------//

# //----------------------------------------------------------------------------------------------//
# //---------------- CREAR FACTURAS ----------------//
def insertar_factura(id_despacho, fecha_emision, estado_pago):
    try:
        # Configurar la conexión a la base de datos
        connection_string = "DRIVER={{SQL Server}};SERVER={};DATABASE=COPPEX;Trusted_Connection=yes;".format(globales.server_name)
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Calcular la fecha de pago (30 días después de la fecha de emisión)
        fecha_pago = fecha_emision + datetime.timedelta(days=30)

        # Ejecutar el procedimiento almacenado sp_InsertarFactura
        cursor.execute("EXEC sp_InsertarFactura @ID_Despacho={}, @Fecha_emision='{}', @Estado_pago='{}', @Fecha_pago='{}'".format(id_despacho, fecha_emision, estado_pago, fecha_pago))
        
        # Confirmar los cambios
        connection.commit()
        
        print("Factura insertada correctamente.")

    except pyodbc.Error as e:
        print("Error al insertar la factura:", e)
        connection.rollback()  # Deshacer cambios en caso de error
        time.sleep(10)

    finally:
        # Cerrar cursor y conexión
        cursor.close()
        connection.close()
# //------------------------------------------------//

# //---------------- MOSTRAR FACTURAS ----------------//
def mostrar_facturas():
    try:
        # Establecer la conexión a la base de datos
        connection_string = "DRIVER={{SQL Server}};SERVER={};DATABASE=COPPEX;Trusted_Connection=yes;".format(globales.server_name)
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Ejecutar el procedimiento almacenado
        cursor.execute("Select * from Factura;")

        # Obtener nombres de las columnas
        columnas = [desc[0] for desc in cursor.description]

        # Obtener todos los resultados
        resultados = cursor.fetchall()

        # Calcular el ancho máximo para cada columna
        anchos = [len(col) for col in columnas]
        for fila in resultados:
            for i, valor in enumerate(fila):
                anchos[i] = max(anchos[i], len(str(valor)))

        # Crear un formato de cadena para cada fila
        formato = ' | '.join([f'{{:<{anchos[i]}}}' for i in range(len(anchos))])

        # Imprimir nombres de las columnas
        print(formato.format(*columnas))
        print('-' * (sum(anchos) + 3 * (len(anchos) - 1)))  # Línea separadora

        # Imprimir resultados
        for fila in resultados:
            print(formato.format(*map(str, fila)))

    except pyodbc.Error as e:
        print(f"Error al mostrar las facturas: {e}")

    finally:
        # Cerrar cursor y conexión
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
# //--------------------------------------------------//

# //---------------- MODIFICAR FACTURAS ----------------//
def modificarfactura(id_factura, nuevo_estado_pago):
    try:
        # Configurar la conexión a la base de datos
        connection_string = "DRIVER={{SQL Server}};SERVER={};DATABASE=COPPEX;Trusted_Connection=yes;".format(globales.server_name)
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Ejecutar el procedimiento almacenado
        cursor.execute("EXEC modificarFactura @ID_Factura=?, @NuevoEstadoPago=?", id_factura, nuevo_estado_pago)
        
        # Confirmar los cambios
        connection.commit()
        
        print("Estado de pago actualizado correctamente.")

    except pyodbc.Error as e:
        print("Error al cambiar el estado de pago de la factura:", e)
        connection.rollback()  # Deshacer cambios en caso de error

    finally:
        # Cerrar cursor y conexión
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
# //----------------------------------------------------//

# //---------------- BUSCAR FACTURA POR ID ----------------//
def buscar_factura(id_factura):
    connection = pyodbc.connect("DRIVER={{SQL Server}};SERVER={};DATABASE=COPPEX;Trusted_Connection=yes;".format(globales.server_name))
    cursor = connection.cursor()
    
    try:
        # Construir la consulta SQL
        sql = "EXEC SeleccionarFactura @ID_Factura = {}".format(id_factura)
        cursor.execute(sql)
        
        # Obtener nombres de las columnas
        columnas = [desc[0] for desc in cursor.description]
        
        # Obtener el resultado
        resultado = cursor.fetchone()
        
        if resultado:
            # Calcular el ancho máximo para cada columna
            anchos = [len(col) for col in columnas]
            for i, valor in enumerate(resultado):
                anchos[i] = max(anchos[i], len(str(valor)))
            
            # Crear un formato de cadena para la fila
            formato = ' | '.join([f'{{:<{anchos[i]}}}' for i in range(len(anchos))])
            
            # Imprimir nombres de las columnas
            print(formato.format(*columnas))
            print('-' * (sum(anchos) + 3 * (len(anchos) - 1)))  # Línea separadora
            
            # Imprimir el resultado
            print(formato.format(*map(str, resultado)))
        else:
            print(f"No se encontró una factura con ID {id_factura}")
            time.sleep(4)
            factura.facturacion()

    except Exception as e:
        print("Error al buscar la factura:", e)
        import traceback
        print(traceback.format_exc())
        time.sleep(4)
        factura.facturacion()
    
    finally:
        # Cerrar cursor y conexión
        cursor.close()
        connection.close()
# //-------------------------------------------------------//
