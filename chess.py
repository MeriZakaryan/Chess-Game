#!/usr/bin/env python3

class Piece:
    def __init__(self, color):
        self.color = color
    
    def move(self, board, from_pos, to_pos): # from_pos = (x1, y1) is tuple then to_pos = (x2, y2)
        # x is like OX (a, b, c, d, e, f, g, h)
        # y is like OY (1, 2, 3, 4, 5, 6, 7, 8)
        x1, y1 = from_pos
        x2, y2 = to_pos
        board[y2][x2] = board[y1][x1]
        board[y1][x1] = None

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
            print(8 - i, end=" ")
            for j in range(8):
                piece = self.board[i][j]
                if piece is None:
                    print("--", end=" ")
                else:
                    print(piece.symbol(), end=" ")
            print("\n")    
        print("  a  b  c  d  e  f  g  h")
     

class Rook(Piece):
    def symbol(self):
        return "wR" if self.color == "white" else "bR"
    
    def move(self, board, from_pos, to_pos):
        y1, x1 = from_pos
        y2, x2 = to_pos

        # check if the path is clear
        if x1 == x2: # vertical direction
            step = 1 if y1 < y2 else -1
            for y in range(y1+step, y2, step):
                if board[y][x1] is not None and board[y][x1].color == self.color:
                    print("Error: path is blocked")
                    return False
        elif y1 == y2: #horizontal direction
            step = 1 if x1 < x2 else -1
            for x in range(x1+step, x2, step):
                if board[y1][x] is not None and board[y1][x].color == self.color:
                    print("Error: path is blocked")
                    return False
        else:
            print("Error. Movement in straight line is required")
            return False
        
        if board[y2][x2] is None or board[y2][x2].color != self.color:
            board[y2][x2] = board[y1][x1]
            board[y1][x1] = None
            return True




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



def user_to_matrix(pos):
    # a1 = (7, 0)
    x, y = list(pos)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    return 8-int(y), letters.index(x)

def main():
    board = Board()
    board.setup()
    # board.board[6][0] = None # this line I wrote for checking if the rook moves in a right way
    board.show_board() 

    user_from = input("Enter figure's position e.g. a1: ")
    user_to = input("Enter where to move e.g. a5: ")

    from_pos = user_to_matrix(user_from)
    to_pos = user_to_matrix(user_to)

    piece = board.board[from_pos[0]][from_pos[1]]
    if piece is not None:
        piece.move(board.board, from_pos, to_pos)
    
    board.show_board()

main()




'''
Guys we have the issue that in console game user enters e.g. a1 then a4, but the program should get it as matrix 
indices a1 -> [7, 0] where a is 0 it is column and 7 is a row. The rows are vice versa :(

As the indices would have to be changed after user input, I've already decided to write user inputs 
If there are other suggestions please heeeeellllppppp
'''