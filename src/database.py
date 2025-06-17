import mysql.connector
from mysql.connector import Error
import config

class Database:
    def __init__(self):
        self.connection = None
    
    import mysql.connector
from mysql.connector import Error
import config
import time

class Database:
    def __init__(self):
        self.connection = None
        self.max_retries = 3
        self.retry_delay = 2  # segundos

    def connect(self):
        """Establece conexión con reintentos automáticos"""
        for attempt in range(self.max_retries):
            try:
                self.connection = mysql.connector.connect(
                    host=config.DB_HOST,
                    user=config.DB_USER,
                    password=config.DB_PASSWORD,
                    database=config.DB_NAME,
                    auth_plugin='mysql_native_password',
                    connect_timeout=5,
                    autocommit=False
                )
                print("✅ Conexión exitosa a MySQL")
                return self.connection
            except Error as e:
                print(f"⚠️ Intento {attempt + 1} fallido: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    print("❌ No se pudo conectar después de varios intentos")
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