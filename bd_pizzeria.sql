DROP DATABASE IF EXISTS pizzeria_flask;
CREATE DATABASE pizzeria_flask;
USE pizzeria_flask;

CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    telefono VARCHAR(20) NOT NULL
);

CREATE TABLE pizzas (
    id_pizza INT AUTO_INCREMENT PRIMARY KEY,
    tamano VARCHAR(20) NOT NULL,
    ingredientes VARCHAR(200) NOT NULL,
    precio DECIMAL(8,2) NOT NULL
);

CREATE TABLE pedidos (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    fecha DATE NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_pedidos_clientes
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        ON DELETE CASCADE
);

CREATE TABLE detalle_pedido (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_pizza INT NOT NULL,
    cantidad INT NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_detalle_pedido_pedidos
        FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido)
        ON DELETE CASCADE,
    CONSTRAINT fk_detalle_pedido_pizzas
        FOREIGN KEY (id_pizza) REFERENCES pizzas(id_pizza)
        ON DELETE CASCADE
);

INSERT INTO clientes (nombre, direccion, telefono) VALUES
('Carlos Mendoza', 'Av. Tecnologico 123', '4771112233'),
('Ana Lopez', 'Calle Hidalgo 45', '4775558899');

INSERT INTO pizzas (tamano, ingredientes, precio) VALUES
('Mediana', 'Jamón', 90.00),
('Grande', 'Jamón, Piña', 140.00),
('Chica', 'Piña', 50.00),
('Grande', 'Jamón, Piña, Champiñones', 150.00);

INSERT INTO pedidos (id_cliente, fecha, total) VALUES
(1, '2026-03-09', 180.00),
(2, '2026-02-13', 240.00);

INSERT INTO detalle_pedido (id_pedido, id_pizza, cantidad, subtotal) VALUES
(1, 1, 2, 180.00),
(2, 2, 1, 140.00),
(2, 3, 2, 100.00);