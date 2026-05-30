# ============================================================
# models/devolucion.py - Modelo de Devolución
# ============================================================
# Maneja todas las operaciones de BD para la tabla 'devoluciones'.
# Las devoluciones se cargan desde BD a la estructura Pila en el controller.
# ============================================================

from config import get_connection


class DevolucionModel:
    """
    Clase que encapsula todas las operaciones de base de datos
    relacionadas con la tabla 'devoluciones'.
    """

    @staticmethod
    def obtener_pendientes():
        """
        Retorna todas las devoluciones con estado 'pendiente'.
        Estas se cargarán en la Pila (LIFO).
        Ordenadas por fecha ascendente para que al hacer push()
        la más reciente quede en la cima.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT d.id, d.pedido_id, d.motivo, d.estado, d.fecha
            FROM devoluciones d
            WHERE d.estado = 'pendiente'
            ORDER BY d.fecha ASC
        """)

        filas = cursor.fetchall()
        conn.close()

        devoluciones = []
        for fila in filas:
            devoluciones.append({
                "id":        fila[0],
                "pedido_id": fila[1],
                "motivo":    fila[2],
                "estado":    fila[3],
                "fecha":     str(fila[4])
            })
        return devoluciones

    @staticmethod
    def obtener_todas():
        """
        Retorna todas las devoluciones (pendientes y revisadas).
        Se usa para mostrar el historial completo.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT d.id, d.pedido_id, d.motivo, d.estado, d.fecha
            FROM devoluciones d
            ORDER BY d.fecha DESC
        """)

        filas = cursor.fetchall()
        conn.close()

        devoluciones = []
        for fila in filas:
            devoluciones.append({
                "id":        fila[0],
                "pedido_id": fila[1],
                "motivo":    fila[2],
                "estado":    fila[3],
                "fecha":     str(fila[4])
            })
        return devoluciones

    @staticmethod
    def crear(pedido_id, motivo):
        """
        Registra una nueva devolución en la BD con estado 'pendiente'.
        Después se hace push() en la Pila en memoria.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO devoluciones (pedido_id, motivo, estado)
            VALUES (?, ?, 'pendiente')
        """, (pedido_id, motivo))

        conn.commit()

        # Obtenemos el ID de la devolución recién creada
        cursor.execute("SELECT @@IDENTITY")
        nuevo_id = int(cursor.fetchone()[0])
        conn.close()

        return nuevo_id

    @staticmethod
    def marcar_revisada(devolucion_id):
        """
        Cambia el estado de una devolución a 'revisada'.
        Se llama cuando hacemos pop() en la Pila.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE devoluciones SET estado = 'revisada' WHERE id = ?
        """, (devolucion_id,))

        conn.commit()
        conn.close()

    @staticmethod
    def contar_pendientes():
        """
        Retorna cuántas devoluciones están pendientes.
        Se usa en el dashboard.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM devoluciones WHERE estado = 'pendiente'")
        total = cursor.fetchone()[0]
        conn.close()

        return total
