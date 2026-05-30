# ============================================================
# data_structures/pila.py - Estructura de datos: PILA (Stack)
# ============================================================
# Una Pila es una estructura LIFO: Last In, First Out.
# El último en entrar es el primero en salir.
#
# Analogía: una pila de platos. Siempre agarras el plato
#           que está encima (el último que pusiste).
#
# En este proyecto: las DEVOLUCIONES se gestionan con una pila.
# La última devolución registrada es la primera en revisarse.
# ============================================================


class NodoPila:
    """
    Representa un elemento individual dentro de la pila.
    Cada nodo guarda un dato y apunta al nodo que estaba debajo de él.
    """
    def __init__(self, dato):
        self.dato = dato      # El valor almacenado (una devolución)
        self.abajo = None     # Referencia al nodo que está debajo en la pila


class Pila:
    """
    Implementación de una Pila (Stack) usando nodos enlazados.
    Operaciones principales:
      - push:    agregar encima
      - pop:     sacar de encima
      - peek:    ver la cima sin sacarla
    """

    def __init__(self):
        # cima: apunta al elemento más reciente (el que saldrá primero)
        self.cima = None
        # tamanio: cuántos elementos tiene la pila
        self.tamanio = 0

    def esta_vacia(self):
        """Retorna True si la pila no tiene elementos."""
        return self.tamanio == 0

    def push(self, dato):
        """
        Agrega un nuevo elemento EN LA CIMA de la pila.
        Esto representa registrar una nueva devolución.
        El nuevo elemento queda encima de todos los demás.
        """
        nuevo_nodo = NodoPila(dato)
        # El nuevo nodo apunta al que antes era la cima
        nuevo_nodo.abajo = self.cima
        # El nuevo nodo ahora ES la cima
        self.cima = nuevo_nodo
        self.tamanio += 1

    def pop(self):
        """
        Elimina y retorna el elemento de LA CIMA de la pila.
        Esto representa tomar la devolución más reciente para revisarla.
        Retorna None si la pila está vacía.
        """
        if self.esta_vacia():
            return None

        # Guardamos el dato de la cima para retornarlo
        dato_cima = self.cima.dato

        # La nueva cima es el elemento que estaba debajo
        self.cima = self.cima.abajo
        self.tamanio -= 1
        return dato_cima

    def peek(self):
        """
        Retorna el elemento de la cima SIN eliminarlo.
        Útil para ver qué devolución se revisará a continuación.
        """
        if self.esta_vacia():
            return None
        return self.cima.dato

    def a_lista(self):
        """
        Convierte la pila a una lista de Python.
        El orden es de cima a base (el primero es el más reciente).
        Útil para mostrar todas las devoluciones en el frontend.
        """
        resultado = []
        nodo_actual = self.cima
        while nodo_actual is not None:
            resultado.append(nodo_actual.dato)
            nodo_actual = nodo_actual.abajo
        return resultado

    def __len__(self):
        """Permite usar len(pila) para obtener el tamaño."""
        return self.tamanio

    def __repr__(self):
        """Representación en texto de la pila (para debugging)."""
        return f"Pila({self.a_lista()})"
