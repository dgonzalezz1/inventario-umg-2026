# ============================================================
# models/pedido.py - Modelo de Pedido
# ============================================================
# Maneja todas las operaciones de BD para la tabla 'pedidos'.
# Los pedidos se cargan desde BD a la estructura Cola en el controller.
# ============================================================

from config import get_connection


class PedidoModel:
    """
    Clase que encapsula todas las operaciones de base de datos
    relacionadas con la tabla 'pedidos'.
    """

    @staticmethod
    def obtener_pendientes():
        """
        Retorna todos los pedidos con estado 'pendiente'.
        Estos son los que se cargarán en la Cola (FIFO).
        Ordenados por fecha ascendente: el más antiguo primero.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.id, pr.nombre AS producto, p.cantidad, p.estado, p.fecha
            FROM pedidos p
            JOIN productos pr ON p.producto_id = pr.id
            WHERE p.estado = 'pendiente'
            ORDER BY p.fecha ASC
        """)

        filas = cursor.fetchall()
        conn.close()

        pedidos = []
        for fila in filas:
            pedidos.append({
                "id":       fila[0],
                "producto": fila[1],
                "cantidad": fila[2],
                "estado":   fila[3],
                "fecha":    str(fila[4])
            })
        return pedidos

    @staticmethod
    def obtener_todos():
        """
        Retorna todos los pedidos (pendientes y procesados).
        Se usa para mostrar el historial completo.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.id, pr.nombre AS producto, p.cantidad, p.estado, p.fecha
            FROM pedidos p
            JOIN productos pr ON p.producto_id = pr.id
            ORDER BY p.fecha DESC
        """)

        filas = cursor.fetchall()
        conn.close()

        pedidos = []
        for fila in filas:
            pedidos.append({
                "id":       fila[0],
                "producto": fila[1],
                "cantidad": fila[2],
                "estado":   fila[3],
                "fecha":    str(fila[4])
            })
        return pedidos

    @staticmethod
    def crear(producto_id, cantidad):
        """
        Inserta un nuevo pedido en la BD con estado 'pendiente'.
        Después de crearlo, también se agrega a la Cola en memoria.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO pedidos (producto_id, cantidad, estado)
            VALUES (?, ?, 'pendiente')
        """, (producto_id, cantidad))

        conn.commit()

        # Obtenemos el ID del pedido recién creado para retornarlo
        cursor.execute("SELECT @@IDENTITY")
        nuevo_id = int(cursor.fetchone()[0])
        conn.close()

        return nuevo_id

    @staticmethod
    def marcar_procesado(pedido_id):
        """
        Cambia el estado de un pedido a 'procesado'.
        Se llama cuando hacemos dequeue() en la Cola.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE pedidos SET estado = 'procesado' WHERE id = ?
        """, (pedido_id,))

        conn.commit()
        conn.close()

    @staticmethod
    def contar_pendientes():
        """
        Retorna cuántos pedidos están pendientes.
        Se usa en el dashboard.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM pedidos WHERE estado = 'pendiente'")
        total = cursor.fetchone()[0]
        conn.close()

        return total
