"""Métodos de búsqueda en el espacio de estados.

Problema P = (I, O, M):
    I: posición teórica B (paso 0).
    O: moverse ΔH a la derecha o a la izquierda y palpar.
    M: posición en la que el palpado detecta la perforación roscada (punto A).
"""

from collections import deque
from dataclasses import dataclass, field

from .modelo import (ALTURA_ANILLO_MM, LIMITE_PASOS, RADIO_INFLUENCIA_ANILLO_MM,
                     CaraLateralBlock, detecta_perforacion)
from .robot import BrazoRobotico

POSICION_INICIAL = 0


@dataclass
class RegistroIteracion:
    """Contenido de las listas abierta y cerrada al comenzar una iteración."""
    numero: int
    abierta: list  # tuplas (paso, h) — h es None en la búsqueda exhaustiva
    cerrada: list


@dataclass
class ResultadoBusqueda:
    metodo: str
    paso_meta: int | None
    palpados: int
    recorrido_mm: float
    traza: list = field(default_factory=list)

    @property
    def encontro_meta(self) -> bool:
        return self.paso_meta is not None

    @property
    def factor_dispersion(self) -> float:
        """P = d / N: longitud de la trayectoria sobre nodos generados (0 ≤ P ≤ 1)."""
        if not self.encontro_meta or self.palpados == 0:
            return 0.0
        return abs(self.paso_meta) / self.palpados


def sucesores(paso: int) -> list[int]:
    """Estados alcanzables con un único operador, respetando el margen explorado."""
    return [vecino for vecino in (paso + 1, paso - 1) if abs(vecino) <= LIMITE_PASOS]


def _resultado(metodo, paso_meta, brazo, traza=None) -> ResultadoBusqueda:
    return ResultadoBusqueda(metodo, paso_meta, brazo.palpados, brazo.recorrido_mm, traza or [])


# ---------------------------------------------------------------------------
# Búsqueda exhaustiva
# ---------------------------------------------------------------------------
def busqueda_primero_en_anchura(cara: CaraLateralBlock) -> ResultadoBusqueda:
    """Método elegido para la búsqueda exhaustiva. Lista abierta FIFO (cola).

    Sin información del dominio, recorre el espacio por niveles: sobre la
    horizontal H esto produce un barrido alternado de amplitud creciente
    a ambos lados de B, que encuentra la posición de A más cercana a B.
    """
    metodo = "Primero en anchura"
    brazo = BrazoRobotico(cara)
    if detecta_perforacion(brazo.mover_y_palpar(POSICION_INICIAL)):
        return _resultado(metodo, POSICION_INICIAL, brazo)

    abierta = deque([POSICION_INICIAL])
    cerrada = []
    generados = {POSICION_INICIAL}
    traza = []

    while abierta:
        traza.append(RegistroIteracion(len(traza) + 1,
                                       [(paso, None) for paso in abierta], list(cerrada)))
        actual = abierta.popleft()
        cerrada.append(actual)
        for sucesor in sucesores(actual):
            if sucesor in generados:
                continue
            generados.add(sucesor)
            if detecta_perforacion(brazo.mover_y_palpar(sucesor)):
                return _resultado(metodo, sucesor, brazo, traza)
            abierta.append(sucesor)

    return _resultado(metodo, None, brazo, traza)


def busqueda_primero_en_profundidad(cara: CaraLateralBlock,
                                    profundidad_limite: int = LIMITE_PASOS) -> ResultadoBusqueda:
    """Alternativa descartada, incluida solo para justificar la elección de anchura.

    Lista abierta LIFO (pila) con profundidad límite. Recorre una rama completa
    antes de retroceder: si empieza por el lado equivocado, llega al límite
    antes de volver hacia A.
    """
    metodo = "Primero en profundidad"
    brazo = BrazoRobotico(cara)
    abierta = [(POSICION_INICIAL, 0)]
    visitados = set()

    while abierta:
        actual, profundidad = abierta.pop()
        if actual in visitados:
            continue
        visitados.add(actual)
        if detecta_perforacion(brazo.mover_y_palpar(actual)):
            return _resultado(metodo, actual, brazo)
        if profundidad < profundidad_limite:
            # Se apilan en orden inverso para explorar primero hacia la derecha.
            for sucesor in reversed(sucesores(actual)):
                if sucesor not in visitados:
                    abierta.append((sucesor, profundidad + 1))

    return _resultado(metodo, None, brazo)


# ---------------------------------------------------------------------------
# Búsqueda heurística
# ---------------------------------------------------------------------------
def heuristica_distancia_estimada(lectura_mm: float) -> float:
    """h(n): distancia estimada desde la posición palpada hasta A.

    Se invierte el perfil conocido del anillo, cuya altura crece al acercarse
    a la perforación: relieve = H·(1 − r/R)  ⇒  r = R·(1 − relieve/H).
    """
    relieve_acotado = min(max(lectura_mm, 0.0), ALTURA_ANILLO_MM)
    return RADIO_INFLUENCIA_ANILLO_MM * (1 - relieve_acotado / ALTURA_ANILLO_MM)


def busqueda_primero_el_mejor(cara: CaraLateralBlock) -> ResultadoBusqueda:
    """Método elegido para la búsqueda heurística, con f(n) = h(n).

    La lista abierta se reordena en forma creciente según h y siempre se
    expande el nodo más prometedor. Si el camino elegido empeora, se retoma
    otro nodo que había quedado en la lista abierta (retroceso).
    En este espacio cada posición se palpa una única vez, por lo que h de un
    nodo no cambia y no hace falta reemplazar valores en abierta ni cerrada.
    """
    metodo = "Primero el mejor"
    brazo = BrazoRobotico(cara)
    lectura_inicial = brazo.mover_y_palpar(POSICION_INICIAL)
    if detecta_perforacion(lectura_inicial):
        return _resultado(metodo, POSICION_INICIAL, brazo)

    abierta = [(POSICION_INICIAL, heuristica_distancia_estimada(lectura_inicial))]
    cerrada = []
    generados = {POSICION_INICIAL}
    traza = []

    while abierta:
        abierta.sort(key=lambda nodo: (nodo[1], nodo[0]))
        traza.append(RegistroIteracion(len(traza) + 1, list(abierta), list(cerrada)))
        actual, _ = abierta.pop(0)
        cerrada.append(actual)
        for sucesor in sucesores(actual):
            if sucesor in generados:
                continue
            generados.add(sucesor)
            lectura = brazo.mover_y_palpar(sucesor)
            if detecta_perforacion(lectura):
                return _resultado(metodo, sucesor, brazo, traza)
            abierta.append((sucesor, heuristica_distancia_estimada(lectura)))

    return _resultado(metodo, None, brazo, traza)
