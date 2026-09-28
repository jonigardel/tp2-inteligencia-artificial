"""Brazo robótico: ejecuta los operadores del problema y registra su costo físico."""

from .modelo import CaraLateralBlock, DELTA_H_MM, paso_a_mm


class BrazoRobotico:
    """Aplica el operador "moverse a una posición y palpar".

    Lleva dos métricas que en la planta equivalen a tiempo de parada:
    la cantidad de palpados (nodos generados) y el recorrido total del brazo.
    """

    def __init__(self, cara: CaraLateralBlock):
        self._cara = cara
        self._posicion_paso = 0
        self.palpados = 0
        self.recorrido_mm = 0.0

    def mover_y_palpar(self, paso_destino: int) -> float:
        self.recorrido_mm += abs(paso_destino - self._posicion_paso) * DELTA_H_MM
        self._posicion_paso = paso_destino
        self.palpados += 1
        return self._cara.distancia_al_plano_patron(paso_a_mm(paso_destino))
