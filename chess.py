class Piece:
    def __init__(self, color):
        self.color = color


class Board:
    def __init__(self):
        for i in range(8):
            row = []
            for cell in range(8):
                row.append(None)
            self.board.append(row)
    
    def is_empty(self, x, y):
        return self.board[x][y] is None
    


class King(Piece):
    pass

class Queen(Piece):
    pass

class Bishop(Piece):
    pass

class Knight(Piece):
    pass

class Rook(Piece):
    pass

class Pawn(Piece):
    pass

