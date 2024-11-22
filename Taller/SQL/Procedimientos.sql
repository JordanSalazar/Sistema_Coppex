-----------------------------------------------------
-- PROCEDIMIENTO PARA ACTUALIZAR DATOS DE CLIENTES --
CREATE PROCEDURE ActualizarAtributoCliente
    @ID_Cliente INT,
    @Atributo NVARCHAR(50),
    @Valor NVARCHAR(MAX)
AS
BEGIN
    DECLARE @sql NVARCHAR(MAX);
    
    SET @sql = N'UPDATE Clientes SET ' + QUOTENAME(@Atributo) + N' = @Valor WHERE ID_Cliente = @ID_Cliente';
    
    EXEC sp_executesql @sql, N'@ID_Cliente INT, @Valor NVARCHAR(MAX)', @ID_Cliente, @Valor;
END;

-----------------------------------------------------
-----------------------------------------------------


-----------------------------------------------------
----- PROCEDIMIENTO DE ALMACENADO PARA PRODUCTOS ----
CREATE PROCEDURE InsertarProducto
    @Nombre VARCHAR(50),
    @Descripcion VARCHAR(200),
    @Precio_Uni INT,
    @Fecha_vencimiento DATE,
    @ID_Categoria INT,
    @Cantidad INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Insertar en la tabla Productos
    INSERT INTO Productos (Nombre, Descripcion, Precio_Uni, Fecha_vencimiento, ID_Categoria)
    VALUES (@Nombre, @Descripcion, @Precio_Uni, @Fecha_vencimiento, @ID_Categoria);

    -- Obtener el ID_Productos generado
    DECLARE @ID_Productos INT;
    SET @ID_Productos = SCOPE_IDENTITY();

    -- Insertar en la tabla Inventario
    INSERT INTO Inventario (ID_Productos, Stock)
    VALUES (@ID_Productos, @Cantidad);

    -- Opcional: Retornar el ID_Productos generado o cualquier otro resultado necesario
    SELECT @ID_Productos AS ID_Productos;

END;
-----------------------------------------------------
-----------------------------------------------------


-----------------------------------------------------
------ PROCEDIMIENTO PARA ACTUALIZAR PRODUCTOS ------
CREATE PROCEDURE ActualizarProducto
    @ID_Producto INT,
    @Atributo VARCHAR(50),
    @Nuevo_Valor SQL_VARIANT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @sql NVARCHAR(MAX);
    DECLARE @TipoDato NVARCHAR(50);
    DECLARE @Tabla NVARCHAR(50);

    -- Determinar la tabla y el tipo de dato del atributo
    IF @Atributo = 'Stock'
    BEGIN
        SET @Tabla = 'Inventario';
        SET @TipoDato = 'int';
    END
    ELSE
    BEGIN
        SELECT @TipoDato = DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'Productos'
        AND COLUMN_NAME = @Atributo;

        IF @TipoDato IS NULL
        BEGIN
            RAISERROR ('El atributo especificado no existe en la tabla Productos.', 16, 1);
            RETURN;
        END
        
        SET @Tabla = 'Productos';
    END

    -- Construir la consulta din�mica para actualizar el atributo especificado
    SET @sql = '
    UPDATE ' + @Tabla + '
    SET ' + QUOTENAME(@Atributo) + ' = CONVERT(' + @TipoDato + ', @Nuevo_Valor)
    WHERE ID_Productos = @ID_Producto;
    ';

    -- Ejecutar la consulta din�mica
    EXEC sp_executesql @sql, N'@ID_Producto INT, @Nuevo_Valor SQL_VARIANT', @ID_Producto, @Nuevo_Valor;

    -- Verificar el n�mero de filas afectadas
    IF @@ROWCOUNT > 0
        PRINT 'Atributo ' + @Atributo + ' actualizado correctamente para el producto con ID ' + CAST(@ID_Producto AS VARCHAR);
    ELSE
        PRINT 'No se encontr� ning�n producto con ID ' + CAST(@ID_Producto AS VARCHAR) + ' o el atributo ' + @Atributo + ' no se actualiz�.';
END;
-----------------------------------------------------
-----------------------------------------------------


-----------------------------------------------------
------ PROCEDIMIENTO PARA VISUALIZAR PRODUCTOS ------
CREATE PROCEDURE VisualizarInventarioProductos
AS
BEGIN
    SET NOCOUNT ON;

    -- Consulta para obtener detalles de los productos y su inventario
    SELECT 
        P.ID_Productos AS ID_Producto,
        P.Nombre AS Nombre_Producto,
        P.Precio_Uni AS Precio_Unitario,
		I.Stock AS Cantidad_Disponible,
        P.Fecha_vencimiento AS Fecha_Caducidad,
        I.ID_invent AS ID_Inventario

    FROM Productos P
    INNER JOIN Inventario I ON P.ID_Productos = I.ID_Productos;

END;
-----------------------------------------------------
-----------------------------------------------------


-----------------------------------------------------
------ PROCEDIMIENTO PARA VISUALIZAR UN PRODUCTO ------

CREATE PROCEDURE BuscarProductoPorID
    @ID_Producto INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Consulta para obtener detalles de un producto espec�fico y su inventario
    SELECT 
        P.ID_Productos AS ID_Producto,
        P.Nombre AS Nombre_Producto,
        P.Precio_Uni AS Precio_Unitario,
        I.Stock AS Cantidad_Disponible,
        P.Fecha_vencimiento AS Fecha_Caducidad,
        I.ID_invent AS ID_Inventario
    FROM Productos P
    INNER JOIN Inventario I ON P.ID_Productos = I.ID_Productos
    WHERE P.ID_Productos = @ID_Producto;

    -- Verificar si se encontr� el producto
    IF @@ROWCOUNT = 0
        PRINT 'No se encontr� ning�n producto con el ID especificado.';
END;

-----------------------------------------------------
-----------------------------------------------------

CREATE TYPE TipoProductoCantidad AS TABLE
(
    ID_Producto INT,
    Cantidad INT
)

----------------------------------------------------------------------------
------ PROCEDIMIENTO PARA CREAR GUIA DE DESPACHO Y ALMACENAR PRODUCTO ------
CREATE PROCEDURE sp_InsertarGuiaYProductosDespacho
    @Fecha_emision DATE,
    @Direccion VARCHAR(50),
    @ID_Cliente INT,
    @Productos TipoProductoCantidad READONLY
AS
BEGIN
    DECLARE @ID_Guia_desp INT, @ID_Despacho INT;
    DECLARE @Precio_Uni INT, @ID_invent INT, @Subtotal INT, @Cantidad_Disponible INT, @IVA INT;

    BEGIN TRY
        -- Iniciar una transacci�n
        BEGIN TRANSACTION;

        -- Insertar en Guia_despacho
        INSERT INTO Guia_despacho (Fecha_emision, Direcci�n)
        VALUES (@Fecha_emision, @Direccion);

        -- Obtener el ID de la gu�a de despacho reci�n insertada
        SET @ID_Guia_desp = SCOPE_IDENTITY();

        -- Insertar en Despacho
        INSERT INTO Despacho (ID_Cliente, ID_Guia_desp, Fecha_venta, Sub_total, IVA, Descuento, Total)
        VALUES (@ID_Cliente, @ID_Guia_desp, @Fecha_emision, 0, 0, 0, 0);

        -- Obtener el ID del despacho reci�n insertado
        SET @ID_Despacho = SCOPE_IDENTITY();

        -- Iterar sobre los productos y cantidades proporcionados
        DECLARE @ID_Producto INT, @Cantidad INT;
        DECLARE cur CURSOR FOR SELECT ID_Producto, Cantidad FROM @Productos;
        OPEN cur;
        FETCH NEXT FROM cur INTO @ID_Producto, @Cantidad;

        WHILE @@FETCH_STATUS = 0
        BEGIN
            -- Obtener el precio unitario del producto
            SELECT @Precio_Uni = Precio_Uni
            FROM Productos
            WHERE ID_Productos = @ID_Producto;

            -- Obtener el ID del inventario correspondiente al producto y la cantidad disponible
            SELECT @ID_invent = ID_invent, @Cantidad_Disponible = Stock
            FROM Inventario
            WHERE ID_Productos = @ID_Producto;

            -- Comprobar si la cantidad ingresada es mayor a la cantidad disponible
            IF @Cantidad > @Cantidad_Disponible
            BEGIN
                RAISERROR ('La cantidad ingresada es mayor a la cantidad disponible en inventario.', 16, 1);
                ROLLBACK TRANSACTION;
                RETURN;
            END

            -- Insertar el detalle del despacho
            INSERT INTO Detalle_despacho (ID_Despacho, ID_invent, Cant_Producto)
            VALUES (@ID_Despacho, @ID_invent, @Cantidad);

            -- Calcular el subtotal
            SET @Subtotal = @Cantidad * @Precio_Uni;

            -- Calcular el IVA (19% del subtotal)
            SET @IVA = ROUND(@Subtotal * 0.19, 0);

            -- Actualizar el subtotal, IVA y total en la tabla Despacho
            UPDATE Despacho
            SET Sub_total = Sub_total + @Subtotal,
                IVA = IVA + @IVA,
                Total = Total + @Subtotal + @IVA
            WHERE ID_Despacho = @ID_Despacho;

            -- Reducir la cantidad en inventario
            UPDATE Inventario
            SET Stock = Stock - @Cantidad
            WHERE ID_invent = @ID_invent;

            FETCH NEXT FROM cur INTO @ID_Producto, @Cantidad;
        END
        CLOSE cur;
        DEALLOCATE cur;

        -- Confirmar la transacci�n
        COMMIT TRANSACTION;

        -- Devolver los valores generados y calculados
        SELECT @ID_Guia_desp AS ID_Guia_desp, @ID_Despacho AS ID_Despacho;

    END TRY
    BEGIN CATCH
        -- En caso de error, deshacer la transacci�n
        ROLLBACK TRANSACTION;
        
        -- Re-lanzar el error
        THROW;
    END CATCH
END

----------------------------------------------------------------------------
----------------------------------------------------------------------------


----------------------------------------------
------ PROCEDIMIENTO PARA MOSTRAR GUIAS ------
CREATE PROCEDURE sp_MostrarDatosGuiaDespacho
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        gd.ID_Guia_desp AS ID_guia_desp,
        c.Razon_social AS Nombre_cliente,
        gd.Fecha_emision,
        d.Total
    FROM
        Guia_despacho gd
        INNER JOIN Despacho d ON gd.ID_Guia_desp = d.ID_Guia_desp
        INNER JOIN Clientes c ON d.ID_Cliente = c.ID_Cliente;
END
----------------------------------------------
----------------------------------------------

-----------------------------------------------------
------ PROCEDIMIENTO PARA MOSTRAR DETALLE GUIA ------
CREATE PROCEDURE sp_MostrarDetalleDespachoCompleto
    @ID_Despacho INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        inv.ID_invent,
        inv.ID_Productos,
        dd.Cant_Producto,
        (dd.Cant_Producto * p.Precio_Uni) AS Sub_total,
        ((dd.Cant_Producto * p.Precio_Uni) * 0.19) AS IVA,
        ((dd.Cant_Producto * p.Precio_Uni) + ((dd.Cant_Producto * p.Precio_Uni) * 0.19)) AS Total
    FROM
        Despacho d
        INNER JOIN Detalle_despacho dd ON d.ID_Despacho = dd.ID_Despacho
        INNER JOIN Inventario inv ON dd.ID_invent = inv.ID_invent
        INNER JOIN Productos p ON inv.ID_Productos = p.ID_Productos
    WHERE
        d.ID_Despacho = @ID_Despacho;
END
-----------------------------------------------------
-----------------------------------------------------

------------------------------------------------
------ PROCEDIMIENTO PARA AGREGAR FACTURA ------
CREATE PROCEDURE sp_InsertarFactura
    @ID_Despacho INT,
    @Fecha_emision DATE,
    @Estado_pago VARCHAR(50),
    @Fecha_pago DATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Insertar datos en la tabla Factura
    INSERT INTO Factura (ID_Despacho, Fecha_emision, Estado_pago, Fecha_pago, Monto_total)
    SELECT @ID_Despacho, @Fecha_emision, @Estado_pago, @Fecha_pago, Total
    FROM Despacho
    WHERE ID_Despacho = @ID_Despacho;

    -- Ejemplo de mensaje de �xito
    SELECT 'Factura insertada correctamente.' AS Resultado;
END
------------------------------------------------
------------------------------------------------

-------------------------------------------------
------ PROCEDIMIENTO PARA MOSTRAR FACTURAS ------
CREATE PROCEDURE modificarFactura
    @ID_Factura INT,
    @NuevoEstadoPago VARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;

    -- Actualizar el estado de pago en la tabla Factura
    UPDATE Factura
    SET Estado_pago = @NuevoEstadoPago
    WHERE ID_Factura = @ID_Factura;

    -- Ejemplo de mensaje de �xito
    SELECT 'Estado de pago actualizado correctamente.' AS Resultado;
END
-------------------------------------------------
-------------------------------------------------

----------------------------------------------------
------ PROCEDIMIENTO PARA MOSTRAR UNA FACTURA ------
CREATE PROCEDURE SeleccionarFactura
    @ID_Factura INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Seleccionar la factura espec�fica basada en el ID
    SELECT
        ID_Factura,
        ID_Despacho,
        Fecha_emision,
        Estado_pago,
        Fecha_pago,
        Monto_total
    FROM
        Factura
    WHERE
        ID_Factura = @ID_Factura;
END
----------------------------------------------------
----------------------------------------------------
