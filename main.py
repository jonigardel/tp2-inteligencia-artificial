"""TP2 - Inteligencia Artificial: búsqueda exhaustiva y heurística.

Ejecutar con:  python main.py
"""

from dataclasses import dataclass

from busqueda.algoritmos import (busqueda_primero_el_mejor, busqueda_primero_en_anchura,
                                 busqueda_primero_en_profundidad)
from busqueda.modelo import CaraLateralBlock
from busqueda.reporte import imprimir_resumen, imprimir_traza


@dataclass(frozen=True)
class Escenario:
    nombre: str
    desplazamiento_mm: float
    inclinacion_por_giro: float = 0.0
    ruido_sensor_mm: float = 0.0
    semilla: int = 1

    def crear_cara(self) -> CaraLateralBlock:
        """Cada búsqueda recibe una cara nueva, con la misma secuencia de ruido."""
        return CaraLateralBlock(self.desplazamiento_mm, self.inclinacion_por_giro,
                                self.ruido_sensor_mm, self.semilla)


ESCENARIOS = [
    Escenario("Escenario 1: desplazamiento de -3,0 mm", -3.0),
    Escenario("Escenario 2: -3,0 mm con giro sobre Z y ruido del sensor", -3.0,
              inclinacion_por_giro=0.08, ruido_sensor_mm=0.2, semilla=3),
    Escenario("Escenario 3: desplazamiento de +12,0 mm (fuera del anillo)", 12.0),
]

METODOS_COMPARADOS = [
    busqueda_primero_en_anchura,
    busqueda_primero_en_profundidad,
    busqueda_primero_el_mejor,
]


def titulo(texto: str) -> None:
    print(f"\n{'=' * 90}\n{texto}\n{'=' * 90}")


def main() -> None:
    escenario_base, escenario_con_ruido, _ = ESCENARIOS

    titulo(f"Búsqueda exhaustiva primero en anchura — {escenario_base.nombre}")
    imprimir_traza(busqueda_primero_en_anchura(escenario_base.crear_cara()))

    titulo(f"Búsqueda heurística primero el mejor — {escenario_base.nombre}")
    imprimir_traza(busqueda_primero_el_mejor(escenario_base.crear_cara()))

    titulo(f"Búsqueda heurística primero el mejor — {escenario_con_ruido.nombre}")
    imprimir_traza(busqueda_primero_el_mejor(escenario_con_ruido.crear_cara()))

    titulo("Comparación de métodos por escenario")
    for escenario in ESCENARIOS:
        print(f"\n{escenario.nombre}")
        for metodo in METODOS_COMPARADOS:
            imprimir_resumen(metodo(escenario.crear_cara()))


if __name__ == "__main__":
    main()
