from scripts.solver import Solver
class Backtracker:
    def __init__(self, board):
        self.board = board
        self.cols_occupied = [False] * self.board.n
        self.rows_occupied=[False]*self.board.n
        self.soluciones_encontradas=[]
    def _get_empty_positions(self):
        free_rows = []
        free_cols = []
        empty_positions = []
        for i in range(self.board.n):
            if self.rows_occupied[i] == False:
                free_rows.append(i)
            if self.cols_occupied[i] == False:
                free_cols.append(i)

        return free_rows, free_cols
    def _recursive_resolve(self, row_index, free_rows, free_cols):
        if row_index == len(free_rows):
            self.soluciones_encontradas.append(list(self.board.queens))
            return False
        actual_row = free_rows[row_index]
        for col in free_cols:
            if self.cols_occupied[col] == False and self.board.is_safe(actual_row, col):
                self.board.place_queen(actual_row, col)
                self.cols_occupied[col] = True
                self._recursive_resolve(row_index + 1, free_rows, free_cols)
                self.board.remove_queen(actual_row, col)
                self.cols_occupied[col] = False
        return False

    def complete_board(self):
        free_rows, free_cols=self._get_empty_positions()
        return self._recursive_resolve(0, free_rows, free_cols)
