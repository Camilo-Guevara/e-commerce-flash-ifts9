
sql
CREATE DATABASE IF NOT EXISTS ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE ecommerce_db;

-- ======================
-- 1) TABLA USUARIO
-- ======================
CREATE TABLE Usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(120) UNIQUE NOT NULL,
    rol ENUM('Cliente','Empleado','Administrador') DEFAULT 'Cliente',
    passwordHash CHAR(128) NOT NULL,
    passwordSalt CHAR(32) NOT NULL,
    fechaRegistro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ======================
-- 2) TABLA PRODUCTO
-- ======================
CREATE TABLE Producto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    descripcion TEXT,
    categoria ENUM('Ropa','Calzado','Accesorios','Otros') DEFAULT 'Otros',
    precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
    stock INT NOT NULL CHECK (stock >= 0),
    imagenURL VARCHAR(255),
    destacado BOOLEAN DEFAULT FALSE,
    nuevo BOOLEAN DEFAULT FALSE,
    fechaAlta DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ======================
-- 3) TABLA PEDIDO
-- ======================
CREATE TABLE Pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idUsuario INT NOT NULL,
    fechaPedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('Abierto','EnProceso','Reservado','Finalizado','Cancelado') DEFAULT 'Abierto',
    total DECIMAL(12,2) DEFAULT 0,
    FOREIGN KEY (idUsuario) REFERENCES Usuario(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ======================
-- 4) TABLA ITEMPEDIDO
-- ======================
CREATE TABLE ItemPedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idPedido INT NOT NULL,
    idProducto INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precioUnitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(12,2) GENERATED ALWAYS AS (cantidad * precioUnitario) STORED,
    FOREIGN KEY (idPedido) REFERENCES Pedido(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (idProducto) REFERENCES Producto(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ======================
-- 5) TRIGGER: Control de stock
-- ======================
DELIMITER //
CREATE TRIGGER trg_reducir_stock
AFTER INSERT ON ItemPedido
FOR EACH ROW
BEGIN
    UPDATE Producto
    SET stock = stock - NEW.cantidad
    WHERE id = NEW.idProducto AND stock >= NEW.cantidad;
END //
DELIMITER ;

-- ======================
-- 6) TRIGGER: Calcular total del pedido
-- ======================
DELIMITER //
CREATE TRIGGER trg_actualizar_total
AFTER INSERT ON ItemPedido
FOR EACH ROW
BEGIN
    UPDATE Pedido
    SET total = (
        SELECT SUM(subtotal) FROM ItemPedido WHERE idPedido = NEW.idPedido
    )
    WHERE id = NEW.idPedido;
END //
DELIMITER ;

-- ======================
CREATE OR REPLACE VIEW vista_pedidos_completos AS
SELECT 
    p.id AS pedido_id,
    u.correo AS usuario,
    p.estado,
    p.fecha_creacion,
    SUM(i.subtotal) AS total_calculado
FROM pedidos p
JOIN usuarios u ON p.id_usuario = u.id
LEFT JOIN item_pedido i ON p.id = i.id_pedido
GROUP BY p.id;
-- ======================