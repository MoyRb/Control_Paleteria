create database paleteria_db;
use paleteria_db;

CREATE TABLE ingredientes (
    id_ingrediente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    cantidad_disponible DECIMAL(10, 2) NOT NULL,
    unidad_medida VARCHAR(20) NOT NULL, -- Ej: kg, litros, unidades
    costo_por_unidad DECIMAL(10, 2) NOT NULL,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE recetas (
    id_receta INT AUTO_INCREMENT PRIMARY KEY,
    nombre_paleta VARCHAR(50) NOT NULL,
    descripcion TEXT,
    costo_produccion DECIMAL(10, 2), -- Se calcula automáticamente
    precio_venta DECIMAL(10, 2) NOT NULL
);

CREATE TABLE receta_ingredientes (
    id_receta INT,
    id_ingrediente INT,
    cantidad_utilizada DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_receta) REFERENCES recetas(id_receta),
    FOREIGN KEY (id_ingrediente) REFERENCES ingredientes(id_ingrediente),
    PRIMARY KEY (id_receta, id_ingrediente)
);

CREATE TABLE ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_receta INT,
    cantidad INT NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_receta) REFERENCES recetas(id_receta)
);

CREATE TABLE gastos (
    id_gasto INT AUTO_INCREMENT PRIMARY KEY,
    concepto VARCHAR(100) NOT NULL, -- Ej: "Compra de azúcar", "Pago de luz"
    monto DECIMAL(10, 2) NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    categoria VARCHAR(50) -- Ej: "Materia prima", "Servicios"
);



