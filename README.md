# N-Queens-Entropy-Randomized-Backtracking
A hybrid n-Queens solver that places the vast majority of queens using randomized entropy distributions and resolves the final edge cases with a localized backtracking algorithm.

# Files Structure
```text
.
├── README.md             # Documento principal con la descripción, instalación y uso del proyecto.
├── scripts/              # Módulos lógicos y matemáticos centrales del algoritmo.
│   ├── __init__.py       # Archivo que define el directorio como un paquete Python importable.
│   ├── backtracking.py   # Fase 2: Algoritmo DFS para resolver los huecos finales conflictivos.
│   ├── board.py          # Maneja el estado del tablero y valida celdas seguras en tiempo constante O(1).
│   ├── queenon.py        # Base matemática: Genera la matriz de probabilidad para la colocación.
│   ├── solver.py         # Fase 1: Ejecuta la colocación aleatoria masiva basada en probabilidad.
│   └── visualizer.py     # Funciones para renderizar el tablero en consola o exportar su gráfica.
├── src/                  # Directorio del punto de entrada de la aplicación.
│   └── main.py           # Script principal; configura el tablero, orquesta las fases y muestra el resultado.
└── tests/                # Pruebas unitarias para garantizar la estabilidad del código.
    ├── __init__.py       # Archivo necesario para que las herramientas de testing reconozcan el directorio.
    └── test8x8.py        # Pruebas a pequeña escala (8x8) para validar que no haya reinas atacándose.

```

<img width="401" height="376" alt="image" src="https://github.com/user-attachments/assets/c3b7685a-6e62-4746-8d65-2e2cdd9324a9" />
