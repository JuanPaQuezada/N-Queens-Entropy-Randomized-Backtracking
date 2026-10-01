class Board:
    def __init__(self, n):
        self.n=n
        self.queens=[]

        #que el board sea un lista de booleanos unidemensionales
        self.board=[False for _ in range(n*n)]
        self.rows_occupied=[False]*n
        self.columns_occupied=[False]*n
        self.principal_diagonal=[False]*(2*n-1)
        self.secondary_diagonal=[False]*(2*n-1)

    def is_safe(self, row, col):
        if self.rows_occupied[row]==False and self.columns_occupied[col]==False and self.principal_diagonal[row-col+self.n-1]==False and self.secondary_diagonal[row+col]==False:
            return True
        return False
    def place_queen(self, row, col):
        self.board[row*self.n+col]=True
        self.rows_occupied[row]=True
        self.columns_occupied[col]=True
        self.principal_diagonal[row-col+self.n-1]=True
        self.secondary_diagonal[row+col]=True
        self.queens.append((row, col))

    def remove_queen(self,row,col):
        self.rows_occupied[row]=False
        self.columns_occupied[col]=False
        self.principal_diagonal[row-col+self.n-1]=False
        self.secondary_diagonal[row+col]=False
        self.queens.remove((row,col))
