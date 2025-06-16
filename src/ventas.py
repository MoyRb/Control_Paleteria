from database import conectar
from datetime import datetime

class VentasManager:
    def registrar_venta(self, id_receta, cantidad):
        conexion = conectar()
        cursor = conexion.cursor()
        
        try:
            # Obtener precio de la receta
            cursor.execute("SELECT precio_venta FROM recetas WHERE id_receta = %s", (id_receta,))
            precio_venta = cursor.fetchone()[0]
            total = precio_venta * cantidad
            
            # Registrar venta
            query = """
            INSERT INTO ventas (id_receta, cantidad, total)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (id_receta, cantidad, total))
            conexion.commit()
            
            # El trigger se encargará de actualizar el inventario
            return True
        except Exception as e:
            conexion.rollback()
            print(f"Error al registrar venta: {e}")
            return False
        finally:
            conexion.close()
    
    def obtener_ventas_por_periodo(self, fecha_inicio, fecha_fin):
        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)
        
        query = """
        SELECT v.*, r.nombre_paleta 
        FROM ventas v
        JOIN recetas r ON v.id_receta = r.id_receta
        WHERE v.fecha BETWEEN %s AND %s
        ORDER BY v.fecha
        """
        cursor.execute(query, (fecha_inicio, fecha_fin))
        return cursor.fetchall()