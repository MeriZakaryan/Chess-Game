#!/usr/bin/env python3

class Piece:
    def __init__(self, color):
        self.color = color

class Board:
    def __init__(self):
        self.board = []
        for i in range(8):
            row = []
            for cell in range(8):
                row.append(None)
            self.board.append(row)
    
    def is_empty(self, x, y):
        return self.board[x][y] is None
    
    def setup(self):
        figures = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for x, figure in enumerate(figures): # enumerate takes an array's element and its index
            self.board[0][x] = figure("black")
            self.board[1][x] = Pawn("black")

        for x, figure in enumerate(figures):
            self.board[6][x] = Pawn("white")
            self.board[7][x] = figure("white")
        
    def show_board(self):
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece is None:
                    print("--", end=" ")
                else:
                    print(piece.symbol(), end=" ")
            print("\n")
     

class Pawn(Piece):
    def symbol(self):
        return "wP" if self.color == "white" else "bP"
    
    

class King(Piece):
    def symbol(self):
        return "wK" if self.color == "white" else "bK"

class Queen(Piece):
    def symbol(self):
        return "wQ" if self.color == "white" else "bQ"

class Bishop(Piece):
    def symbol(self):
        return "wB" if self.color == "white" else "bB"

class Knight(Piece):
    def symbol(self):
        return "wN" if self.color == "white" else "bN"

class Rook(Piece):
    def symbol(self):
        return "wR" if self.color == "white" else "bR"


board = Board()
board.setup()
board.show_board() 