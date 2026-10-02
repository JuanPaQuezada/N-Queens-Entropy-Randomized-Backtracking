import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from scripts.board import Board
from scripts.solver import Solver
from scripts.backtracking import Backtracker
from scripts.visualizer import plot_board, iniciar_visor

def main():
    n=8
    board = Board(n) 
    rescate=Backtracker(board)
    all_solutions=rescate.complete_board()
    print(f"Total solutions found: {len(all_solutions)}")
    if len(all_solutions)>0:
        first_solution=all_solutions[0]
        iniciar_visor(all_solutions, n)
if __name__ == "__main__":
    main()
