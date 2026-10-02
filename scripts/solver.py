import math
from queenon import get_coordinates, entropy_concave
import random
class Solver:
    def __init__(self, board):
        self.board = board
        self.coordinates, self.probabilities = entropy_concave(board)
        self.queens_limit=self.board.n-math.sqrt(self.board.n)
        self.consecutive_failures = 0
    def get_next_moves(self):
        while len(self.board.queens)<self.queens_limit:
            next_move = random.choices(self.coordinates, weights=self.probabilities, k=1)[0]
            row, col = next_move 
            if self.board.is_safe(row, col):
                self.board.place_queen(row, col)
                self.consecutive_failures = 0
            else:
                self.consecutive_failures += 1
                if self.consecutive_failures > 100:
                    break
            
