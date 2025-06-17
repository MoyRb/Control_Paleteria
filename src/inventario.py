import mysql.connector
from mysql.connector import Error
from typing import Tuple, List, Dict, Union

class Inventario:
    """Clase para gestionar el inventario de ingredientes y productos de la paletería."""
    
    def __init__(self, conexion):
        """Inicializa la clase con una conexión a la base de datos.
        
        Args:
            conexion: Objeto de conexión a MySQL
        """
        self.conexion = conexion
    
    # Métodos para ingredientes
    def agregar_ingrediente(self, nombre: str, cantidad: float, unidad_medida: str, 
                          costo_por_unidad: float, stock_minimo: float) -> Tuple[bool, str]:
        """Agrega un nuevo ingrediente al inventario.
        
        Args:
            nombre: Nombre del ingrediente
            cantidad: Cantidad disponible
            unidad_medida: Unidad de medida (kg, litros, etc.)
            costo_por_unidad: Costo por unidad de medida
            stock_minimo: Nivel mínimo de stock para alertas
            
        Returns:
            Tuple con (success, message)
        """
        try:
            with self.conexion.cursor() as cursor:
                query = """INSERT INTO ingredientes 
                          (nombre, cantidad, unidad_medida, costo_por_unidad, stock_minimo) 
                          VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(query, (nombre, cantidad, unidad_medida, costo_por_unidad, stock_minimo))
                self.conexion.commit()
                return True, "Ingrediente agregado correctamente"
        except Error as e:
            print(f"Error al agregar ingrediente: {e}")
            return False, f"Error al agregar ingrediente: {e}"
    
    def actualizar_ingrediente(self, id_ingrediente: int, **kwargs) -> Tuple[bool, str]:
        """Actualiza los datos de un ingrediente existente.
        
        Args:
            id_ingrediente: ID del ingrediente a actualizar
            kwargs: Campos a actualizar (nombre, cantidad, unidad_medida, etc.)
            
        Returns:
            Tuple con (success, message)
        """
        if not kwargs:
            return False, "No se proporcionaron datos para actualizar"
            
        try:
            with self.conexion.cursor() as cursor:
                set_clause = ", ".join([f"{key} = %s" for key in kwargs])
                query = f"UPDATE ingredientes SET {set_clause} WHERE id_ingrediente = %s"
                values = list(kwargs.values()) + [id_ingrediente]
                
                cursor.execute(query, values)
                self.conexion.commit()
                return True, "Ingrediente actualizado correctamente"
        except Error as e:
            print(f"Error al actualizar ingrediente: {e}")
            return False, f"Error al actualizar ingrediente: {e}"
    
    def obtener_ingredientes(self, filtros: Dict = None) -> Union[List[Dict], Tuple[bool, str]]:
        """Obtiene la lista de ingredientes con opción a filtrar.
        
        Args:
            filtros: Diccionario con campos para filtrar (opcional)
            
        Returns:
            Lista de ingredientes o tuple con (False, error) en caso de fallo
        """
        try:
            with self.conexion.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM ingredientes"
                params = []
                
                if filtros:
                    where_clauses = []
                    for key, value in filtros.items():
                        where_clauses.append(f"{key} = %s")
                        params.append(value)
                    query += " WHERE " + " AND ".join(where_clauses)
                
                cursor.execute(query, params)
                return cursor.fetchall()
        except Error as e:
            print(f"Error al obtener ingredientes: {e}")
            return False, f"Error al obtener ingredientes: {e}"
    
    def verificar_stock(self, id_receta: int, cantidad: int) -> Tuple[bool, str]:
        """Verifica si hay suficiente stock para preparar una cantidad de recetas.
        
        Args:
            id_receta: ID de la receta a verificar
            cantidad: Cantidad de veces a preparar la receta
            
        Returns:
            Tuple con (success, message)
        """
        try:
            with self.conexion.cursor(dictionary=True) as cursor:
                query = """SELECT i.id_ingrediente, i.nombre, i.cantidad as stock_actual, 
                          ri.cantidad * %s as cantidad_necesaria, i.unidad_medida
                          FROM ingredientes i
                          JOIN receta_ingredientes ri ON i.id_ingrediente = ri.id_ingrediente
                          WHERE ri.id_receta = %s"""
                cursor.execute(query, (cantidad, id_receta))
                resultados = cursor.fetchall()
                
                for item in resultados:
                    if item['stock_actual'] < item['cantidad_necesaria']:
                        faltante = item['cantidad_necesaria'] - item['stock_actual']
                        return False, (f"Stock insuficiente de {item['nombre']}. "
                                      f"Faltan {faltante} {item['unidad_medida']}")
                return True, "Stock suficiente para la producción"
        except Error as e:
            print(f"Error al verificar stock: {e}")
            return False, f"Error al verificar stock: {e}"
    
    def alertas_stock_bajo(self) -> Union[List[Dict], Tuple[bool, str]]:
        """Obtiene los ingredientes con stock por debajo del mínimo establecido.
        
        Returns:
            Lista de ingredientes con stock bajo o tuple con (False, error)
        """
        try:
            with self.conexion.cursor(dictionary=True) as cursor:
                query = """SELECT id_ingrediente, nombre, cantidad, stock_minimo, unidad_medida 
                          FROM ingredientes 
                          WHERE cantidad < stock_minimo"""
                cursor.execute(query)
                return cursor.fetchall()
        except Error as e:
            print(f"Error al obtener alertas de stock: {e}")
            return False, f"Error al obtener alertas de stock: {e}"
    
    # Métodos adicionales recomendados
    def ajustar_inventario(self, id_ingrediente: int, cantidad: float, 
                         motivo: str = "Ajuste manual") -> Tuple[bool, str]:
        """Ajusta el inventario de un ingrediente (incrementa o decrementa).
        
        Args:
            id_ingrediente: ID del ingrediente
            cantidad: Cantidad a ajustar (positivo para agregar, negativo para restar)
            motivo: Razón del ajuste (para registro histórico)
            
        Returns:
            Tuple con (success, message)
        """
        # Implementación similar a actualizar_ingrediente pero con registro histórico
        pass
    
    def obtener_movimientos(self, id_ingrediente: int = None, 
                          fecha_inicio: str = None, fecha_fin: str = None) -> Union[List[Dict], Tuple[bool, str]]:
        """Obtiene el historial de movimientos de inventario.
        
        Args:
            id_ingrediente: Filtrar por ingrediente (opcional)
            fecha_inicio: Fecha de inicio para filtrar (opcional)
            fecha_fin: Fecha de fin para filtrar (opcional)
            
        Returns:
            Lista de movimientos o tuple con (False, error)
        """
        # Implementación para consultar tabla de historial
        pass