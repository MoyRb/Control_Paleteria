import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="marlen17",
        database="paleteria_db"
    )

# Ejemplo: Insertar un ingrediente
def agregar_ingrediente(nombre, cantidad, unidad, costo):
    conexion = conectar()
    cursor = conexion.cursor()
    query = "INSERT INTO ingredientes (nombre, cantidad_disponible, unidad_medida, costo_por_unidad) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (nombre, cantidad, unidad, costo))
    conexion.commit()
    conexion.close()

def calcular_costo_receta(id_receta):
    conexion = conectar()
    cursor = conexion.cursor()
    query = """
    SELECT SUM(i.costo_por_unidad * ri.cantidad_utilizada) 
    FROM receta_ingredientes ri
    JOIN ingredientes i ON ri.id_ingrediente = i.id_ingrediente
    WHERE ri.id_receta = %s
    """
    cursor.execute(query, (id_receta,))
    costo = cursor.fetchone()[0]
    conexion.close()
    return costo

