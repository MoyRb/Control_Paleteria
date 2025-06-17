class UI:
    def __init__(self, inventario):
        self.inventario = inventario
    
    def mostrar_menu_principal(self):
        while True:
            print("\n--- MENÚ PRINCIPAL ---")
            print("1. Gestión de Inventario")
            print("2. Ventas")
            print("3. Producción")
            print("4. Reportes")
            print("5. Salir")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self.menu_inventario()
            elif opcion == "2":
                print("Módulo de ventas (pendiente)")
            elif opcion == "3":
                print("Módulo de producción (pendiente)")
            elif opcion == "4":
                print("Módulo de reportes (pendiente)")
            elif opcion == "5":
                break
            else:
                print("Opción no válida")
    
    def menu_inventario(self):
        while True:
            print("\n--- GESTIÓN DE INVENTARIO ---")
            print("1. Listar productos")
            print("2. Agregar producto")
            print("3. Actualizar stock")
            print("4. Buscar producto")
            print("5. Volver al menú principal")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self.listar_productos()
            elif opcion == "2":
                self.agregar_producto()
            elif opcion == "3":
                self.actualizar_stock()
            elif opcion == "4":
                self.buscar_producto()
            elif opcion == "5":
                break
            else:
                print("Opción no válida")
    
    def listar_productos(self):
        productos = self.inventario.obtener_productos()
        print("\n--- LISTA DE PRODUCTOS ---")
        for prod in productos:
            print(f"ID: {prod['id']}, Nombre: {prod['nombre']}, Stock: {prod['cantidad_stock']}, Precio: ${prod['precio']}")
    
    def agregar_producto(self):
        print("\n--- AGREGAR PRODUCTO ---")
        nombre = input("Nombre: ")
        descripcion = input("Descripción: ")
        precio = float(input("Precio: "))
        cantidad = int(input("Cantidad inicial: "))
        categoria = input("Categoría: ")
        
        self.inventario.agregar_producto(nombre, descripcion, precio, cantidad, categoria)
        print("Producto agregado exitosamente!")
    
    def actualizar_stock(self):
        self.listar_productos()
        producto_id = int(input("\nID del producto a actualizar: "))
        cantidad = int(input("Cantidad a agregar (use negativo para restar): "))
        
        self.inventario.actualizar_stock(producto_id, cantidad)
        print("Stock actualizado!")
    
    def buscar_producto(self):
        print("\n--- BUSCAR PRODUCTO ---")
        nombre = input("Nombre (dejar vacío para omitir): ")
        categoria = input("Categoría (dejar vacío para omitir): ")
        
        resultados = self.inventario.buscar_producto(nombre or None, categoria or None)
        print("\nResultados de búsqueda:")
        for prod in resultados:
            print(f"ID: {prod['id']}, Nombre: {prod['nombre']}, Categoría: {prod['categoria']}")