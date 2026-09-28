"""Modelo del dominio: la cara lateral del block y el palpado de su relieve.

El prototipo simula solo el movimiento sobre la horizontal H, ya que el
posicionamiento vertical es correcto. Cada estado es una posición del extremo
del brazo expresada en pasos de ΔH respecto de la posición teórica B.
"""

import random

DELTA_H_MM = 0.5
"""Incremento de avance del brazo entre dos estados consecutivos."""

LIMITE_PASOS = 30
"""Máximo desplazamiento explorado a cada lado de B (30 pasos = ±15 mm)."""

ALTURA_ANILLO_MM = 4.0
RADIO_INFLUENCIA_ANILLO_MM = 8.0
RADIO_PERFORACION_MM = 0.25
PROFUNDIDAD_PERFORACION_MM = -10.0
UMBRAL_DETECCION_PERFORACION_MM = -5.0


def paso_a_mm(paso: int) -> float:
    return paso * DELTA_H_MM


def detecta_perforacion(lectura_mm: float) -> bool:
    """Test de meta: el palpador cae dentro de la perforación roscada (punto A)."""
    return lectura_mm < UMBRAL_DETECCION_PERFORACION_MM


class CaraLateralBlock:
    """Cara lateral del block tal como está realmente sobre la cinta.

    El robot no conoce estos parámetros: solo puede palparla en una posición
    y leer la distancia desde el plano patrón hasta la superficie.
    """

    def __init__(self, desplazamiento_mm: float, inclinacion_por_giro: float = 0.0,
                 ruido_sensor_mm: float = 0.0, semilla: int = 1):
        self._posicion_real_de_a_mm = desplazamiento_mm
        self._inclinacion_por_giro = inclinacion_por_giro
        self._ruido_sensor_mm = ruido_sensor_mm
        self._generador_ruido = random.Random(semilla)

    def distancia_al_plano_patron(self, x_mm: float) -> float:
        distancia_a_a = abs(x_mm - self._posicion_real_de_a_mm)
        if distancia_a_a <= RADIO_PERFORACION_MM:
            relieve = PROFUNDIDAD_PERFORACION_MM
        else:
            relieve = ALTURA_ANILLO_MM * max(0.0, 1 - distancia_a_a / RADIO_INFLUENCIA_ANILLO_MM)
        relieve += self._inclinacion_por_giro * x_mm
        if self._ruido_sensor_mm:
            relieve += self._generador_ruido.gauss(0, self._ruido_sensor_mm)
        return relieve
