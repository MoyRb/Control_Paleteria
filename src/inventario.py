import mysql.connector
from mysql.connector import Error

class Inventario:
    def __init__(self, conexion):
        self.conexion = conexion
    
    def agregar_ingrediente(self, nombre, cantidad, unidad_medida, costo_por_unidad, stock_minimo):
        try:
            cursor = self.conexion.cursor()
            query = """INSERT INTO ingredientes 
                      (nombre, cantidad, unidad_medida, costo_por_unidad, stock_minimo) 
                      VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (nombre, cantidad, unidad_medida, costo_por_unidad, stock_minimo))
            self.conexion.commit()
            return True
        except Error as e:
            print(f"Error al agregar ingrediente: {e}")
            return False
    
    def verificar_stock(self, id_receta, cantidad):
        try:
            cursor = self.conexion.cursor(dictionary=True)
            query = """SELECT i.id_ingrediente, i.nombre, i.cantidad as stock_actual, 
                      ri.cantidad * %s as cantidad_necesaria
                      FROM ingredientes i
                      JOIN receta_ingredientes ri ON i.id_ingrediente = ri.id_ingrediente
                      WHERE ri.id_receta = %s"""
            cursor.execute(query, (cantidad, id_receta))
            resultados = cursor.fetchall()
            
            for item in resultados:
                if item['stock_actual'] < item['cantidad_necesaria']:
                    return False, f"Stock insuficiente de {item['nombre']}"
            return True, "Stock suficiente"
        except Error as e:
            print(f"Error al verificar stock: {e}")
            return False, f"Error: {e}"