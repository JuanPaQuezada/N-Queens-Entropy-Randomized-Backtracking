# N-Queens Entropy-Based Randomized Backtracking Solver

This project implements a hybrid solver for the N-Queens problem, combining a probabilistic constructive heuristic inspired by entropy-driven placement strategies from the literature with an exact backtracking repair step designed by the author to guarantee correctness. The central idea is simple but effective: use a biased, randomized strategy to place most queens in positions that are structurally favorable, and then solve the remaining unresolved conflicts using a depth-first search constrained to the exact safety rules of the puzzle.

The solver is not a purely stochastic method and it is not a classical exhaustive backtracking solver either. It is a hybrid strategy that aims to reduce the combinatorial search space while preserving the formal guarantees of exact resolution in the final stage.

---

## 1. Problem definition

The N-Queens problem consists of placing $N$ queens on an $N \times N$ chessboard such that no two queens share the same row, column, or diagonal. This is one of the canonical constraint satisfaction problems. A brute-force enumeration of all candidate placements grows exponentially with $N$, which makes naive search impractical even for moderate board sizes.

The classical exact formulation solves this by maintaining the set of occupied rows and columns and checking diagonal conflicts incrementally. In this repository, that exact logic is preserved and used in a local repair phase, while the probabilistic phase reduces the number of unresolved conflicts before the exact search begins.

---

## 2. Why a hybrid approach?

A pure random placement strategy tends to fail because the constraints are highly coupled: the placement of one queen drastically affects the feasibility of many others. Conversely, a pure exact backtracking search is exhaustive and may explore a large number of partial states before finding a valid configuration.

The hybrid method tries to achieve a balance between these two extremes:

- The probabilistic stage acts as a constructive heuristic. It biases placements toward central and low-risk locations, which are statistically more likely to coexist without producing conflicts.
- The exact stage acts as a correctness layer. Once the heuristic reaches a constrained residual state, the search re-evaluates the remaining free rows and columns under the formal safety constraints and resolves the remaining contradictions deterministically.

This is the key design concept behind the implementation: keep the search guided and sparse, but do not sacrifice correctness.

---

## 3. Paper-inspired component vs. original contribution

This project is explicitly hybrid and the code reflects that distinction clearly.

### 3.1 Paper-inspired probabilistic heuristic

The entropy-like component is implemented primarily in the following files:

- `scripts/queenon.py`
- `scripts/solver.py`

In `queenon.py`, the board is mapped into a normalized continuous coordinate system and a weight is assigned to each cell according to its squared distance from the board center. The logic follows the same conceptual idea used in entropy- or energy-based randomized optimization methods: positions near the center are considered structurally more promising because they reduce conflict overlap with the global symmetry of the board. The code computes a weight distribution and converts it into a probability mass function.

The weighted placement is then sampled in `Solver.get_next_moves()` inside `scripts/solver.py` using `random.choices(...)` with those computed probabilities. In other words, rather than choosing randomly among all cells uniformly, the algorithm biases the search toward cells that are strategically more compatible with a valid global arrangement.

This part is the component that reflects the inspiration from the referenced paper: the solver is not doing blind random placement, but guided stochastic placement based on a structural bias.

### 3.2 Original backtracking layer

The exact and independent repair phase is implemented in:

- `scripts/backtracking.py`
- `scripts/board.py`

This layer is the author’s own complement to the heuristic stage. The board state is maintained with boolean arrays for:

- occupied rows
- occupied columns
- primary diagonals
- secondary diagonals

The method `Board.is_safe(row, col)` checks each candidate in constant time $O(1)$ by verifying the row, column, and both diagonal trackers. This is the formal foundation that allows exact validation without recomputing the entire board.

Then `Backtracker._recursive_resolve()` explores the remaining empty rows and tries feasible columns. When a placement is found, the state is updated; when a conflict arises, the algorithm backtracks and tries another option. This stage is the exact correction mechanism that compensates for the heuristic stage and guarantees that the final solution respects all N-Queens rules.

So, in direct terms:

- The paper-inspired part is the probabilistic, entropy-biased constructive phase.
- The backtracking part is my original exact repair mechanism added to make the solver robust and valid.

---

## 4. Architectural description

### 4.1 Board representation

`Board` in `scripts/board.py` is the state engine of the solver. It stores:

- `self.n`: board size
- `self.queens`: list of placed queens as $(row, col)$ pairs
- `self.board`: flattened board representation
- `self.rows_occupied`: row occupancy mask
- `self.columns_occupied`: column occupancy mask
- `self.principal_diagonal`: main diagonal occupancy mask
- `self.secondary_diagonal`: anti-diagonal occupancy mask

This structure is important because it gives constant-time conflict detection while remaining lightweight and easy to reason about. The implementation avoids scanning the whole board for each placement, which would otherwise degrade performance dramatically.

### 4.2 Heuristic placement stage

`Solver` in `scripts/solver.py` initializes a weighted probability distribution using `entropy_concave(board)`. The key behavior is the following:

1. Each cell is mapped to a normalized coordinate pair around the center.
2. A convex-shaped weight is computed from the squared distance to the center.
3. These weights are normalized into a probability distribution.
4. Candidate positions are sampled according to that distribution.
5. Only safe placements are accepted; otherwise the solver records a failure.
6. The algorithm stops when the number of queens placed is close to the threshold $n - \sqrt{n}$.

The logic behind this threshold is practical rather than purely theoretical. It acknowledges that the exact resolution stage will handle the remaining conflict-heavy cells more effectively than trying to force a fully random completion from the start. In other words, the heuristic is used to reduce the complexity of the residual problem without overcommitting to a fragile greedy strategy.

### 4.3 Exact backtracking repair stage

Once the heuristic stage reaches a partial placement, `Backtracker.complete_board()` in `scripts/backtracking.py` retrieves the currently empty rows and columns and invokes `_recursive_resolve()`.

At each recursive step:

- A free row is selected.
- A candidate free column is tested for safety.
- If the queen can be placed without violating the rules, it is set.
- The function continues recursively.
- If a branch fails, the queen is removed and the search tries another column.

This is a classic depth-first backtracking strategy, but it is local and targeted: it does not search the entire board from scratch; it resolves only the unresolved subset of the problem left by the heuristic phase.

This distinction is essential. The probabilistic phase does not pretend to solve the full problem optimally; it reduces the amount of exact search needed. The backtracking layer restores the validity guarantee.

---

## 5. Why the method works

The hybrid philosophy is grounded in the trade-off between diversification and exactness.

- Randomized placement introduces diversity and helps escape the deterministic bias of entirely greedy methods.
- Probability weighting introduces structure, which is crucial in strongly constrained combinatorial spaces.
- Backtracking restores mathematical correctness by revisiting only the frontier of unresolved conflicts.

This makes the method effective for small and medium board sizes where a pure exact search would otherwise be more expensive, while retaining the formal discipline of a valid solver.

The design also follows a realistic engineering principle: when solving a highly constrained combinatorial optimization problem, it is often better to minimize the search space with a guided heuristic and then enforce exact feasibility via local exhaustive repair.

---

## 6. Complexity analysis

The complexity of the exact N-Queens problem is exponential in the worst case, and this hybrid solver does not change that fundamental fact. However, it improves practical performance by reducing the number of valid configurations that must be explored.

### Heuristic stage

The weighted random placement is bounded by the number of queens inserted before the cutoff, which is approximately $n - \sqrt{n}$ in this implementation. Each candidate placement checks safety in constant time through the occupancy masks.

### Exact repair stage

The backtracking phase remains exponential in the worst case, because the problem is NP-hard in its general form. However, it operates only on the remaining unresolved structure, and therefore it is substantially smaller than solving the entire board from an empty state.

In short, the solver trades a controlled amount of probabilistic guidance for a substantially reduced exact search space.

---

## 7. Repository structure

```text
.
<<<<<<< HEAD
├── README.md
├── requirements.txt
├── scripts/
│   ├── __init__.py
│   ├── backtracking.py      # Exact repair stage with DFS/backtracking
│   ├── board.py             # Safety checks and board state management
│   ├── queenon.py           # Entropy-inspired weighting and probability generation
│   ├── solver.py            # Randomized placement guided by weights
│   └── visualizer.py        # Visualization utilities
├── src/
│   └── main.py              # Program entry point and orchestration
├── tests/
│   ├── __init__.py
│   └── test8x8.py           # Intended validation for small board checks
└── ...
```

---

## 8. Execution

### 8.1 Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 8.2 Run the solver

```bash
python src/main.py
```

This entry point initializes a board, runs the randomized heuristic phase, invokes the backtracking repair phase, and displays the computed solution set.

---

## 9. Validation approach

The correctness criterion is straightforward: each returned solution must satisfy the N-Queens constraints, which means no two queens share a row, column, or diagonal. This is enforced by the board safety logic and validated during backtracking.

The repository includes a minimal testing area under `tests/`, and the design of `Board.is_safe()` makes the validation fast and deterministic. For small boards such as $8 \times 8$, the verifier can easily confirm that all queen positions are non-attacking.

---

## 10. Final assessment

This project demonstrates an engineering-oriented approach to a classical combinatorial problem: keep the initial constructive stage intelligent and stochastic, but leave the final correctness to an exact adaptive search. The result is a robust hybrid solver that respects both the theoretical structure of the puzzle and the practical need for efficient search.

In summary:

- The probabilistic distribution is the paper-inspired heuristic layer.
- The board validation and DFS repair are the original exact layer added for correctness.
- The whole project reflects a realistic computational design: reduce the combinatorial burden first, then enforce feasibility exactly.

This is not just a toy implementation; it is a practical hybrid strategy for a difficult constraint problem.
=======
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
<p align=center>
    <img width="401" height="376" alt="image" src="https://github.com/user-attachments/assets/c3b7685a-6e62-4746-8d65-2e2cdd9324a9" />
</p>
