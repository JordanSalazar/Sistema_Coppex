crear = "create database COPPEX"

clientes = """USE COPPEX;
create table Clientes
(
    ID_Cliente int identity(1,1) primary key,
    Rut varchar(10) not null,
    Razon_social varchar(100) not null,
    Giro varchar(100) not null,
    Correo varchar(50) not null,
    Telefono int not null,
    Fecha_alta date DEFAULT GETDATE() NOT NULL,
    Fecha_baja date NULL
)"""

usuarios = """USE COPPEX;
create table Usuarios
(
	ID_Usuario int identity(1,1) primary key,
	Cargo varchar(20) not null,
	Nombre varchar(15) not null,
	Apellido varchar(15) not null,
	Email varchar(30) not null,
	Pass varchar(15) not null
)"""

categoria = """USE COPPEX;
CREATE TABLE Categoria
(
    ID_Categoria INT IDENTITY(1,1) PRIMARY KEY,
    Tipo VARCHAR(15)
);"""

productos = """USE COPPEX;
CREATE TABLE Productos
(
    ID_Productos INT IDENTITY(1,1) PRIMARY KEY,
    Nombre VARCHAR(20) NOT NULL,
    Descripcion VARCHAR(200) NOT NULL,
    Precio_Uni INT NOT NULL,
    Fecha_vencimiento DATE NOT NULL,
    ID_Categoria INT NOT NULL,
    CONSTRAINT FK_Productos_Categoria FOREIGN KEY (ID_Categoria) REFERENCES Categoria(ID_Categoria)
);"""

inventario = """USE COPPEX;
create table Inventario
(
	ID_invent int IDENTITY(1,1) PRIMARY KEY,
	ID_Productos int not null,
	constraint FK_Productos_inventario FOREIGN KEY (ID_Productos) references Productos(ID_Productos),
	Stock int not null
)"""

guia = """USE COPPEX;
create table Guia_despacho
(
	ID_Guia_desp int IDENTITY(1,1) PRIMARY KEY,
	Fecha_emision date not null,
	Direccion varchar(50) not null
)"""

despacho = """USE COPPEX;
create table Despacho
(
	ID_Despacho int IDENTITY(1,1) PRIMARY KEY,
	ID_Cliente int not null,
	constraint FK_Cliente_despacho foreign key (ID_Cliente) references Clientes(ID_Cliente),
	ID_Guia_desp int not null,
	constraint FK_Guia_desp_despacho foreign key (ID_Guia_desp) references Guia_despacho(ID_Guia_desp),
	Fecha_venta date not null,
	Sub_total int not null,
	IVA int not null,
	Descuento int not null,
	Total int not null
)"""

detalle = """USE COPPEX;
create table Detalle_despacho
(
	ID_Despacho int not null,
	constraint FK_Detalle_despacho foreign key (ID_Despacho) references Despacho(ID_Despacho),
	ID_invent int not null,
	constraint FK_Detalle_invent foreign key (ID_invent) references Inventario(ID_invent),
	Cant_Producto int not null
)"""

factura = """USE COPPEX;
create table Factura
(
	ID_Factura int IDENTITY(1,1) PRIMARY KEY,
	ID_Despacho int not null,
	constraint FK_Factura_Despacho foreign key (ID_Despacho) references Despacho(ID_Despacho),
	Fecha_emision date not null,
	Monto_total int not null,
	Estado_Pago varchar(15) not null,
	Fecha_pago date null
)"""



