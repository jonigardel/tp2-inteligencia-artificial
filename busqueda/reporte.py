"""Presentación de trazas y resultados en consola."""

from .algoritmos import ResultadoBusqueda
from .modelo import paso_a_mm


def _formatear_posicion(paso: int) -> str:
    return f"{paso_a_mm(paso):+.1f}"


def _formatear_nodo(paso: int, h: float | None) -> str:
    posicion = _formatear_posicion(paso)
    return posicion if h is None else f"{posicion}({h:.1f})"


def imprimir_traza(resultado: ResultadoBusqueda) -> None:
    print(f"{'Paso':>4} | {'Abierta':<36} | Cerrada")
    print("-" * 90)
    for registro in resultado.traza:
        abierta = ", ".join(_formatear_nodo(paso, h) for paso, h in registro.abierta)
        cerrada = ", ".join(_formatear_posicion(paso) for paso in registro.cerrada)
        print(f"{registro.numero:>4} | {abierta:<36} | {cerrada}")
    if resultado.encontro_meta:
        print(f"Meta A detectada en {_formatear_posicion(resultado.paso_meta)} mm respecto de B")
    else:
        print("No se detectó la perforación dentro del margen explorado")


def imprimir_resumen(resultado: ResultadoBusqueda) -> None:
    meta = _formatear_posicion(resultado.paso_meta) if resultado.encontro_meta else "  —  "
    print(f"  {resultado.metodo:<24} meta={meta:>6} mm | palpados N={resultado.palpados:>3} | "
          f"recorrido={resultado.recorrido_mm:>6.1f} mm | P=d/N={resultado.factor_dispersion:.2f}")
