# ============================================================
# controllers/inventario_controller.py - Controlador Principal
# ============================================================
# El CONTROLLER es el intermediario entre el Model y la View.
# Recibe las peticiones HTTP, llama al Model para obtener datos,
# usa las estructuras de datos (Cola/Pila) y retorna la respuesta.
#
# Aquí definimos todas las rutas (endpoints) de la aplicación.
# ============================================================

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash

# Importamos los modelos (capa de base de datos)
from app.models.producto   import ProductoModel
from app.models.pedido     import PedidoModel
from app.models.devolucion import DevolucionModel

# Importamos nuestras estructuras de datos
from app.data_structures.cola  import Cola
from app.data_structures.pila  import Pila

# ── Blueprint de Flask ───────────────────────────────────────
# Un Blueprint agrupa rutas relacionadas. Es como un mini-app
# que luego registramos en la app principal.
inventario_bp = Blueprint("inventario", __name__)

# ── Estructuras de datos en memoria ─────────────────────────
# Estas instancias viven mientras el servidor esté corriendo.
# Se recargan con datos de la BD cada vez que se inician.
cola_pedidos     = Cola()   # Cola FIFO para pedidos pendientes
pila_devoluciones = Pila()  # Pila LIFO para devoluciones pendientes


def cargar_estructuras():
    """
    Carga los datos pendientes desde la BD hacia las estructuras en memoria.
    Se llama al iniciar la app para sincronizar BD con Cola/Pila.
    Los pedidos se encolan en orden de fecha (el más antiguo primero).
    Las devoluciones se apilan en orden de fecha (la más reciente queda en la cima).
    """
    global cola_pedidos, pila_devoluciones

    # Reiniciamos las estructuras para evitar duplicados
    cola_pedidos      = Cola()
    pila_devoluciones = Pila()

    # Cargamos pedidos pendientes a la cola (ya vienen ordenados por fecha ASC)
    for pedido in PedidoModel.obtener_pendientes():
        cola_pedidos.enqueue(pedido)

    # Cargamos devoluciones pendientes a la pila (fecha ASC → la última queda en cima)
    for devolucion in DevolucionModel.obtener_pendientes():
        pila_devoluciones.push(devolucion)


# ============================================================
# RUTAS - VISTAS (devuelven páginas HTML)
# ============================================================

@inventario_bp.route("/")
def dashboard():
    """
    Página principal con resumen del sistema.
    Muestra contadores de productos, pedidos y devoluciones.
    """
    resumen = {
        "total_productos":    ProductoModel.contar(),
        "pedidos_pendientes": PedidoModel.contar_pendientes(),
        "devoluciones":       DevolucionModel.contar_pendientes(),
        # Próximo pedido a procesar (peek sin sacar de la cola)
        "proximo_pedido":     cola_pedidos.peek()
    }
    return render_template("index.html", resumen=resumen)


@inventario_bp.route("/productos")
def vista_productos():
    """
    Página que muestra la lista completa de productos.
    El model consulta la BD y retorna una lista de diccionarios.
    """
    productos = ProductoModel.obtener_todos()
    return render_template("productos.html", productos=productos)


@inventario_bp.route("/pedidos")
def vista_pedidos():
    """
    Página de gestión de pedidos.
    Muestra la Cola de pedidos pendientes y el historial completo.
    """
    # Obtenemos la cola como lista para mostrar en el template
    cola_lista   = cola_pedidos.a_lista()
    todos_pedidos = PedidoModel.obtener_todos()
    productos    = ProductoModel.obtener_todos()  # Para el formulario de nuevo pedido

    return render_template(
        "pedidos.html",
        cola=cola_lista,
        pedidos=todos_pedidos,
        productos=productos,
        tamanio_cola=len(cola_pedidos)
    )


@inventario_bp.route("/devoluciones")
def vista_devoluciones():
    """
    Página de gestión de devoluciones.
    Muestra la Pila de devoluciones pendientes y el historial.
    """
    # Convertimos la pila a lista para mostrar (cima primero = más reciente primero)
    pila_lista    = pila_devoluciones.a_lista()
    todas          = DevolucionModel.obtener_todas()
    pedidos_proc  = PedidoModel.obtener_todos()  # Para seleccionar pedido en el form

    return render_template(
        "devoluciones.html",
        pila=pila_lista,
        devoluciones=todas,
        pedidos=pedidos_proc,
        tamanio_pila=len(pila_devoluciones)
    )


# ============================================================
# RUTAS - API REST (devuelven JSON)
# Estas rutas son las que el frontend consulta con fetch/AJAX
# ============================================================

# ── Productos ────────────────────────────────────────────────

@inventario_bp.route("/api/productos", methods=["GET"])
def api_obtener_productos():
    """GET /api/productos → Lista todos los productos en JSON."""
    productos = ProductoModel.obtener_todos()
    return jsonify({"ok": True, "datos": productos})


@inventario_bp.route("/api/productos", methods=["POST"])
def api_crear_producto():
    """
    POST /api/productos → Crea un nuevo producto.
    Espera un JSON con: nombre, descripcion, precio, stock, categoria.
    """
    datos = request.get_json()

    # Validación básica: campos requeridos
    if not datos or not datos.get("nombre") or not datos.get("precio"):
        return jsonify({"ok": False, "mensaje": "Nombre y precio son obligatorios"}), 400

    try:
        ProductoModel.crear(
            nombre      = datos["nombre"],
            descripcion = datos.get("descripcion", ""),
            precio      = float(datos["precio"]),
            stock       = int(datos.get("stock", 0)),
            categoria   = datos.get("categoria", "General")
        )
        return jsonify({"ok": True, "mensaje": "Producto creado correctamente"}), 201

    except Exception as e:
        return jsonify({"ok": False, "mensaje": str(e)}), 500


@inventario_bp.route("/api/productos/<int:producto_id>", methods=["PUT"])
def api_actualizar_producto(producto_id):
    """
    PUT /api/productos/<id> → Actualiza un producto existente.
    Espera un JSON con los campos a actualizar.
    """
    datos = request.get_json()

    if not datos:
        return jsonify({"ok": False, "mensaje": "No se enviaron datos"}), 400

    # Verificamos que el producto existe antes de actualizar
    existente = ProductoModel.obtener_por_id(producto_id)
    if not existente:
        return jsonify({"ok": False, "mensaje": "Producto no encontrado"}), 404

    try:
        ProductoModel.actualizar(
            producto_id = producto_id,
            nombre      = datos.get("nombre",      existente["nombre"]),
            descripcion = datos.get("descripcion", existente["descripcion"]),
            precio      = float(datos.get("precio", existente["precio"])),
            stock       = int(datos.get("stock",   existente["stock"])),
            categoria   = datos.get("categoria",   existente["categoria"])
        )
        return jsonify({"ok": True, "mensaje": "Producto actualizado correctamente"})

    except Exception as e:
        return jsonify({"ok": False, "mensaje": str(e)}), 500


@inventario_bp.route("/api/productos/<int:producto_id>", methods=["DELETE"])
def api_eliminar_producto(producto_id):
    """DELETE /api/productos/<id> → Elimina un producto."""
    existente = ProductoModel.obtener_por_id(producto_id)
    if not existente:
        return jsonify({"ok": False, "mensaje": "Producto no encontrado"}), 404

    try:
        ProductoModel.eliminar(producto_id)
        return jsonify({"ok": True, "mensaje": "Producto eliminado"})
    except Exception as e:
        return jsonify({"ok": False, "mensaje": str(e)}), 500


# ── Pedidos ──────────────────────────────────────────────────

@inventario_bp.route("/api/pedidos", methods=["GET"])
def api_obtener_pedidos():
    """GET /api/pedidos → Estado actual de la cola y todos los pedidos."""
    return jsonify({
        "ok":           True,
        "cola":         cola_pedidos.a_lista(),
        "tamanio_cola": len(cola_pedidos),
        "todos":        PedidoModel.obtener_todos()
    })


@inventario_bp.route("/api/pedidos", methods=["POST"])
def api_crear_pedido():
    """
    POST /api/pedidos → Crea un pedido y lo agrega al FINAL de la cola.
    Operación: enqueue()
    Espera JSON con: producto_id, cantidad.
    """
    datos = request.get_json()

    if not datos or not datos.get("producto_id") or not datos.get("cantidad"):
        return jsonify({"ok": False, "mensaje": "producto_id y cantidad son obligatorios"}), 400

    try:
        # 1. Guardamos en la base de datos
        nuevo_id = PedidoModel.crear(
            producto_id = int(datos["producto_id"]),
            cantidad    = int(datos["cantidad"])
        )

        # 2. Obtenemos el pedido recién creado para agregarlo a la cola en memoria
        pedido_nuevo = {
            "id":       nuevo_id,
            "producto": ProductoModel.obtener_por_id(int(datos["producto_id"]))["nombre"],
            "cantidad": int(datos["cantidad"]),
            "estado":   "pendiente"
        }

        # 3. Hacemos enqueue: agregamos al final de la cola
        cola_pedidos.enqueue(pedido_nuevo)

        return jsonify({
            "ok":           True,
            "mensaje":      "Pedido agregado a la cola",
            "tamanio_cola": len(cola_pedidos)
        }), 201

    except Exception as e:
        return jsonify({"ok": False, "mensaje": str(e)}), 500


@inventario_bp.route("/api/pedidos/procesar", methods=["POST"])
def api_procesar_pedido():
    """
    POST /api/pedidos/procesar → Procesa el PRIMER pedido de la cola.
    Operación: dequeue()
    El pedido sale de la cola y se marca como 'procesado' en la BD.
    """
    if cola_pedidos.esta_vacia():
        return jsonify({"ok": False, "mensaje": "La cola de pedidos está vacía"}), 400

    try:
        # dequeue: sacamos el primer pedido de la cola (el más antiguo)
        pedido_procesado = cola_pedidos.dequeue()

        # Actualizamos su estado en la base de datos
        PedidoModel.marcar_procesado(pedido_procesado["id"])

        return jsonify({
            "ok":              True,
            "mensaje":         f"Pedido #{pedido_procesado['id']} procesado",
            "pedido":          pedido_procesado,
            "tamanio_cola":    len(cola_pedidos),
            "proximo_pedido":  cola_pedidos.peek()
        })

    except Exception as e:
        return jsonify({"ok": False, "mensaje": str(e)}), 500


# ── Devoluciones ─────────────────────────────────────────────

@inventario_bp.route("/api/devoluciones", methods=["GET"])
def api_obtener_devoluciones():
    """GET /api/devoluciones → Estado actual de la pila y todas las devoluciones."""
    return jsonify({
        "ok":            True,
        "pila":          pila_devoluciones.a_lista(),
        "tamanio_pila":  len(pila_devoluciones),
        "todas":         DevolucionModel.obtener_todas()
    })


@inventario_bp.route("/api/devoluciones", methods=["POST"])
def api_crear_devolucion():
    """
    POST /api/devoluciones → Registra una devolución y la pone en la CIMA de la pila.
    Operación: push()
    Espera JSON con: pedido_id, motivo.
    """
    datos = request.get_json()

    if not datos or not datos.get("pedido_id") or not datos.get("motivo"):
        return jsonify({"ok": False, "mensaje": "pedido_id y motivo son obligatorios"}), 400

    try:
        # 1. Guardamos en la base de datos
        nuevo_id = DevolucionModel.crear(
            pedido_id = int(datos["pedido_id"]),
            motivo    = datos["motivo"]
        )

        # 2. Creamos el objeto devolución para la pila en memoria
        devolucion_nueva = {
            "id":        nuevo_id,
            "pedido_id": int(datos["pedido_id"]),
            "motivo":    datos["motivo"],
            "estado":    "pendiente"
        }

        # 3. Hacemos push: la nueva devolución queda en la CIMA de la pila
        pila_devoluciones.push(devolucion_nueva)

        return jsonify({
            "ok":            True,
            "mensaje":       "Devolución registrada en la pila",
            "tamanio_pila":  len(pila_devoluciones)
        }), 201

    except Exception as e:
        return jsonify({"ok": False, "mensaje": str(e)}), 500


@inventario_bp.route("/api/devoluciones/revisar", methods=["POST"])
def api_revisar_devolucion():
    """
    POST /api/devoluciones/revisar → Revisa la devolución de la CIMA de la pila.
    Operación: pop()
    La devolución sale de la pila y se marca como 'revisada' en la BD.
    """
    if pila_devoluciones.esta_vacia():
        return jsonify({"ok": False, "mensaje": "La pila de devoluciones está vacía"}), 400

    try:
        # pop: sacamos la devolución de la cima (la más reciente)
        devolucion_revisada = pila_devoluciones.pop()

        # Actualizamos su estado en la base de datos
        DevolucionModel.marcar_revisada(devolucion_revisada["id"])

        return jsonify({
            "ok":           True,
            "mensaje":      f"Devolución #{devolucion_revisada['id']} revisada",
            "devolucion":   devolucion_revisada,
            "tamanio_pila": len(pila_devoluciones),
            "cima_actual":  pila_devoluciones.peek()
        })

    except Exception as e:
        return jsonify({"ok": False, "mensaje": str(e)}), 500
