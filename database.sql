-- ============================================================
-- SCRIPT SQL - Sistema de Gestión de Inventarios
-- Universidad Mariano Gálvez - Programación III
-- Ejecutar en SQL Server Management Studio (SSMS)
-- ============================================================

-- Crear la base de datos
CREATE DATABASE inventario_db;
GO

USE inventario_db;
GO

-- ============================================================
-- TABLA: productos
-- Almacena todos los productos del inventario
-- ============================================================
CREATE TABLE productos (
    id          INT IDENTITY(1,1) PRIMARY KEY,  -- ID auto-incremental
    nombre      VARCHAR(100) NOT NULL,           -- Nombre del producto
    descripcion VARCHAR(255),                    -- Descripción opcional
    precio      DECIMAL(10, 2) NOT NULL,         -- Precio unitario
    stock       INT NOT NULL DEFAULT 0,          -- Cantidad disponible
    categoria   VARCHAR(50),                     -- Categoría del producto
    fecha_creacion DATETIME DEFAULT GETDATE()    -- Fecha de registro
);
GO

-- ============================================================
-- TABLA: pedidos
-- Almacena los pedidos que entran a la COLA (FIFO)
-- ============================================================
CREATE TABLE pedidos (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    producto_id INT NOT NULL,                    -- Referencia al producto
    cantidad    INT NOT NULL,                    -- Cantidad solicitada
    estado      VARCHAR(20) DEFAULT 'pendiente', -- pendiente / procesado
    fecha       DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);
GO

-- ============================================================
-- TABLA: devoluciones
-- Almacena las devoluciones que se gestionan en la PILA (LIFO)
-- ============================================================
CREATE TABLE devoluciones (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    pedido_id   INT NOT NULL,                    -- Referencia al pedido devuelto
    motivo      VARCHAR(255) NOT NULL,           -- Razón de la devolución
    estado      VARCHAR(20) DEFAULT 'pendiente', -- pendiente / revisada
    fecha       DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
);
GO

-- ============================================================
-- DATOS DE PRUEBA - productos
-- ============================================================
INSERT INTO productos (nombre, descripcion, precio, stock, categoria) VALUES
('Laptop HP 15"',       'Procesador Intel i5, 8GB RAM, 256GB SSD', 5500.00, 10, 'Computadoras'),
('Mouse Inalámbrico',   'Mouse Logitech M185, receptor USB',        180.00,  50, 'Accesorios'),
('Teclado Mecánico',    'Teclado RGB switches azules',              450.00,  30, 'Accesorios'),
('Monitor 24"',         'Full HD 1080p, panel IPS, 75Hz',          1800.00, 15, 'Monitores'),
('Audífonos Bluetooth', 'JBL Tune 510BT, 40 horas de batería',     350.00,  25, 'Audio'),
('Webcam HD',           '1080p con micrófono integrado',           280.00,  20, 'Accesorios'),
('USB Hub 7 puertos',   'USB 3.0, alimentación independiente',     120.00,  40, 'Accesorios'),
('SSD Externo 1TB',     'Samsung T7, USB-C, lectura 1050 MB/s',   850.00,  18, 'Almacenamiento');
GO

-- ============================================================
-- DATOS DE PRUEBA - pedidos
-- ============================================================
INSERT INTO pedidos (producto_id, cantidad, estado) VALUES
(1, 2, 'pendiente'),
(3, 5, 'pendiente'),
(2, 10, 'procesado');
GO

-- ============================================================
-- DATOS DE PRUEBA - devoluciones
-- ============================================================
INSERT INTO devoluciones (pedido_id, motivo, estado) VALUES
(3, 'Producto llegó dañado', 'pendiente'),
(3, 'Talla incorrecta',      'revisada');
GO
