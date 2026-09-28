# TP2 – Búsqueda en el espacio de estados

Simula el posicionamiento del brazo robótico sobre la perforación roscada del block
cuando este quedó desplazado en la cinta transportadora. El robot parte de la posición
teórica **B** y debe encontrar la posición real de montaje **A** moviéndose solo sobre
la horizontal **H**, ya que el posicionamiento vertical es correcto.

## Formulación del problema

| Componente | Definición en el prototipo |
|---|---|
| **I** – estado inicial | Posición teórica B (paso 0) |
| **O** – operadores | Moverse ΔH = 0,5 mm a la derecha o a la izquierda y palpar la superficie |
| **M** – meta | Posición en la que el palpado detecta la perforación roscada (punto A) |

Cada estado es una posición B ± k·ΔH. El espacio se acota a ±15 mm de B.

## Métodos implementados

- **Búsqueda exhaustiva – primero en anchura** (lista abierta FIFO). Es el método elegido:
  como el robot no sabe hacia qué lado está A, el recorrido por niveles produce un barrido
  alternado a ambos lados de B y encuentra la posición más cercana.
- **Búsqueda heurística – primero el mejor**, con f(n) = h(n). Es el método elegido:
  h(n) estima la distancia a A invirtiendo el perfil conocido del anillo prominente
  a partir del relieve palpado.
- **Primero en profundidad** (lista abierta LIFO) se incluye solo como referencia para
  justificar la elección de anchura.

## Escenarios simulados

1. Desplazamiento de −3,0 mm, sin perturbaciones.
2. Desplazamiento de −3,0 mm, con giro del block sobre el eje Z y ruido en el sensor.
3. Desplazamiento de +12,0 mm, fuera del radio en que el relieve del anillo orienta la búsqueda.

Para cada método se informa la cantidad de palpados (nodos generados, N), el recorrido
total del brazo y el factor de dispersión P = d/N.

## Estructura

```
├── main.py                 # Ejecuta las trazas y la comparación de métodos
├── busqueda/
│   ├── modelo.py           # Cara lateral del block, relieve y test de meta
│   ├── robot.py            # Brazo robótico: operador "mover y palpar" y métricas
│   ├── algoritmos.py       # Primero en anchura, primero en profundidad, primero el mejor
│   └── reporte.py          # Impresión de listas abierta/cerrada y resúmenes
```

## Ejecución

Requiere Python 3.10 o superior. No usa dependencias externas.

```bash
python main.py            # trazas de listas abierta/cerrada y tabla comparativa
```
