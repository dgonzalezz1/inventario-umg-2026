# ============================================================
# models/producto.py - Modelo de Producto
# ============================================================
# El MODEL es la capa que se comunica directamente con la BD.
# Solo hace consultas SQL. No conoce Flask ni el frontend.
# Si necesitas cambiar algo de la BD, solo editas este archivo.
# ============================================================

from config import get_connection


class ProductoModel:
    """
    Clase que encapsula todas las operaciones de base de datos
    relacionadas con la tabla 'productos'.
    Cada método abre su propia conexión, hace la consulta y la cierra.
    """

    @staticmethod
    def obtener_todos():
        """
        Retorna una lista con todos los productos de la base de datos.
        Cada producto es un diccionario con sus campos.
        """
        conn = get_connection()
        cursor = conn.cursor()

        # Consulta que trae todos los productos ordenados por nombre
        cursor.execute("""
            SELECT id, nombre, descripcion, precio, stock, categoria, fecha_creacion
            FROM productos
            ORDER BY nombre
        """)

        filas = cursor.fetchall()
        conn.close()

        # Convertimos cada fila a un diccionario para facilitar el uso en templates
        productos = []
        for fila in filas:
            productos.append({
                "id":             fila[0],
                "nombre":         fila[1],
                "descripcion":    fila[2],
                "precio":         float(fila[3]),
                "stock":          fila[4],
                "categoria":      fila[5],
                "fecha_creacion": str(fila[6])
            })
        return productos

    @staticmethod
    def obtener_por_id(producto_id):
        """
        Busca y retorna un único producto por su ID.
        Retorna None si no existe el producto.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nombre, descripcion, precio, stock, categoria
            FROM productos
            WHERE id = ?
        """, (producto_id,))

        fila = cursor.fetchone()
        conn.close()

        if fila is None:
            return None

        return {
            "id":          fila[0],
            "nombre":      fila[1],
            "descripcion": fila[2],
            "precio":      float(fila[3]),
            "stock":       fila[4],
            "categoria":   fila[5]
        }

    @staticmethod
    def crear(nombre, descripcion, precio, stock, categoria):
        """
        Inserta un nuevo producto en la base de datos.
        Los parámetros (?) previenen inyección SQL.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO productos (nombre, descripcion, precio, stock, categoria)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, descripcion, precio, stock, categoria))

        conn.commit()   # Confirma la transacción en la BD
        conn.close()

    @staticmethod
    def actualizar(producto_id, nombre, descripcion, precio, stock, categoria):
        """
        Actualiza los datos de un producto existente.
        Solo modifica el producto que tenga el ID indicado.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE productos
            SET nombre = ?, descripcion = ?, precio = ?, stock = ?, categoria = ?
            WHERE id = ?
        """, (nombre, descripcion, precio, stock, categoria, producto_id))

        conn.commit()
        conn.close()

    @staticmethod
    def eliminar(producto_id):
        """
        Elimina un producto de la base de datos por su ID.
        Precaución: esto también puede afectar pedidos relacionados.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))

        conn.commit()
        conn.close()

    @staticmethod
    def contar():
        """
        Retorna el número total de productos en la BD.
        Se usa en el dashboard para mostrar el resumen.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM productos")
        total = cursor.fetchone()[0]
        conn.close()

        return total
