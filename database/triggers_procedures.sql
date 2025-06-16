-- En triggers_procedures.sql
DELIMITER //
CREATE TRIGGER after_venta_insert
AFTER INSERT ON ventas
FOR EACH ROW
BEGIN
    -- Actualizar el inventario restando los ingredientes usados
    UPDATE ingredientes i
    JOIN receta_ingredientes ri ON i.id_ingrediente = ri.id_ingrediente
    SET i.cantidad_disponible = i.cantidad_disponible - (ri.cantidad_utilizada * NEW.cantidad)
    WHERE ri.id_receta = NEW.id_receta;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE actualizar_costos_produccion()
BEGIN
    UPDATE recetas r
    SET costo_produccion = (
        SELECT SUM(i.costo_por_unidad * ri.cantidad_utilizada)
        FROM receta_ingredientes ri
        JOIN ingredientes i ON ri.id_ingrediente = i.id_ingrediente
        WHERE ri.id_receta = r.id_receta
    );
END //
DELIMITER ;