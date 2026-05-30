# ============================================================
# data_structures/cola.py - Estructura de datos: COLA (Queue)
# ============================================================
# Una Cola es una estructura FIFO: First In, First Out.
# El primero en entrar es el primero en salir.
# 
# Analogía: la fila del banco. El primero en llegar 
#           es el primero en ser atendido.
#
# En este proyecto: los PEDIDOS entran a una cola.
# El pedido más antiguo (primero en entrar) se procesa primero.
# ============================================================


class Nodo:
    """
    Representa un elemento individual dentro de la cola.
    Cada nodo guarda un dato y apunta al siguiente nodo.
    """
    def __init__(self, dato):
        self.dato = dato        # El valor que almacena este nodo (un pedido)
        self.siguiente = None   # Referencia al siguiente nodo en la cola


class Cola:
    """
    Implementación de una Cola (Queue) usando nodos enlazados.
    Operaciones principales:
      - enqueue: agregar al final
      - dequeue: sacar del frente
      - peek:    ver el frente sin sacarlo
    """

    def __init__(self):
        # frente: apunta al primer elemento (el próximo a salir)
        self.frente = None
        # final: apunta al último elemento (el más reciente en entrar)
        self.final = None
        # tamanio: cuenta cuántos elementos hay en la cola
        self.tamanio = 0

    def esta_vacia(self):
        """Retorna True si la cola no tiene elementos."""
        return self.tamanio == 0

    def enqueue(self, dato):
        """
        Agrega un nuevo elemento AL FINAL de la cola.
        Esto representa registrar un nuevo pedido.
        """
        nuevo_nodo = Nodo(dato)

        if self.esta_vacia():
            # Si la cola está vacía, el nuevo nodo es frente Y final
            self.frente = nuevo_nodo
            self.final = nuevo_nodo
        else:
            # Conectamos el nodo actual del final al nuevo nodo
            self.final.siguiente = nuevo_nodo
            # Actualizamos la referencia del final
            self.final = nuevo_nodo

        self.tamanio += 1

    def dequeue(self):
        """
        Elimina y retorna el elemento del FRENTE de la cola.
        Esto representa procesar el pedido más antiguo.
        Retorna None si la cola está vacía.
        """
        if self.esta_vacia():
            return None

        # Guardamos el dato del frente para retornarlo
        dato_frente = self.frente.dato

        # Movemos el frente al siguiente nodo
        self.frente = self.frente.siguiente

        # Si ya no hay frente, tampoco hay final
        if self.frente is None:
            self.final = None

        self.tamanio -= 1
        return dato_frente

    def peek(self):
        """
        Retorna el elemento del frente SIN eliminarlo.
        Útil para ver qué pedido se procesará a continuación.
        """
        if self.esta_vacia():
            return None
        return self.frente.dato

    def a_lista(self):
        """
        Convierte la cola a una lista de Python.
        Útil para mostrar todos los elementos en el frontend.
        El orden es de frente a final (el primero es el más antiguo).
        """
        resultado = []
        nodo_actual = self.frente
        while nodo_actual is not None:
            resultado.append(nodo_actual.dato)
            nodo_actual = nodo_actual.siguiente
        return resultado

    def __len__(self):
        """Permite usar len(cola) para obtener el tamaño."""
        return self.tamanio

    def __repr__(self):
        """Representación en texto de la cola (para debugging)."""
        return f"Cola({self.a_lista()})"
