import mysql.connector
from mysql.connector import Error
import config

class Database:
    def __init__(self):
        self.connection = None
    
    def connect(self):
        """Establece la conexión a la base de datos"""
        try:
            self.connection = mysql.connector.connect(
                host=config.DB_HOST,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                database=config.DB_NAME,
                autocommit=False  # Mejor control con transacciones explícitas
            )
            print("Conexión exitosa a la base de datos")
            return self.connection
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None
    
    def disconnect(self):
        """Cierra la conexión a la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada")
    
    def get_connection(self):
        """Obtiene la conexión actual o establece una nueva"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection