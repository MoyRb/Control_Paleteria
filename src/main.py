from database import Database
from inventario import Inventario
from ui import UI
import sys

def main():
    print("Sistema de Gestión de Paletería - DINOSIS")
    
    # Inicializar la conexión a la base de datos
    db = Database()
    conexion = db.connect()
    
    if not conexion:
        print("No se pudo conectar a la base de datos. Saliendo...")
        sys.exit(1)
    
    try:
        # Inicializar módulos con la conexión
        inventario = Inventario(conexion)
        ui = UI(inventario)
        
        # Mostrar menú principal
        ui.mostrar_menu_principal()
        
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        # Asegurarse de cerrar la conexión al finalizar
        db.disconnect()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAplicación terminada por el usuario")
        sys.exit(0)