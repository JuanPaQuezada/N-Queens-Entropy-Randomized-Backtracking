import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from scripts.board import Board
from scripts.solver import Solver
from scripts.backtracking import Backtracker
from scripts.visualizer import plot_board

def main():
    n=8
    board = Board(n)
    solver = Solver(board)
    solver.get_next_moves()
    print(f"Queens placed: {len(board.queens)}")
   
    rescate=Backtracker(board)
    all_solutions=rescate.complete_board()
    print(f"Total solutions found: {len(rescate.soluciones_encontradas)}")
    if len(all_solutions)>0:
        first_solution=all_solutions[0]
        plot_board(first_solution, n)

if __name__ == "__main__":
    main()
