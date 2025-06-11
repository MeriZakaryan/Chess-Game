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
    
    def move(self, board, from_pos, to_pos):
        y1, x1 = from_pos
        y2, x2 = to_pos

        direction = -1 if self.color == "white" else 1  # White moves up (-1), Black moves down (+1)

        # Basic one step forward move
        if x2 == x1 and y2 == y1 + direction:
            if board[y2][x2] is None:
                board[y2][x2] = board[y1][x1]
                board[y1][x1] = None
                return True
            else:
                print("Error: Pawn cannot move forward to an occupied square")
                return False

        # Two steps forward from starting position
        start_row = 6 if self.color == "white" else 1
        if x2 == x1 and y1 == start_row and y2 == y1 + 2*direction:
            if board[y1 + direction][x1] is None and board[y2][x2] is None:
                board[y2][x2] = board[y1][x1]
                board[y1][x1] = None
                return True
            else:
                print("Error: Path blocked for pawn double move")
                return False

        # Capture diagonally
        if abs(x2 - x1) == 1 and y2 == y1 + direction:
            target = board[y2][x2]
            if target is not None and target.color != self.color:
                board[y2][x2] = board[y1][x1]
                board[y1][x1] = None
                return True
            else:
                print("Error: No opponent piece to capture")
                return False

        print("Error: Invalid pawn move")
        return False    
    

class King(Piece):
    def symbol(self):
        return "wK" if self.color == "white" else "bK"
    
    def move(self, board, from_pos, to_pos):
        y1, x1 = from_pos
        y2, x2 = to_pos

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        # King can move 1 square in any direction
        if dx <= 1 and dy <= 1:
            target_piece = board[y2][x2]
            if target_piece is None or target_piece.color != self.color:
                board[y2][x2] = board[y1][x1]
                board[y1][x1] = None
                return True
            else:
                print("Error: Cannot capture own piece")
                return False
        else:
            print("Error: King can only move 1 square in any direction")
            return False


class Queen(Piece):
    def symbol(self):
        return "wQ" if self.color == "white" else "bQ"
    
    def move(self, board, from_pos, to_pos):
        y1, x1 = from_pos
        y2, x2 = to_pos

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        if x1 == x2:  # vertical
            step = 1 if y1 < y2 else -1
            for y in range(y1 + step, y2, step):
                if board[y][x1] is not None:
                    print("Error: path is blocked")
                    return False
        elif y1 == y2:  # horizontal
            step = 1 if x1 < x2 else -1
            for x in range(x1 + step, x2, step):
                if board[y1][x] is not None:
                    print("Error: path is blocked")
                    return False
        elif dx == dy:  # diagonal
            step_y = 1 if y2 > y1 else -1
            step_x = 1 if x2 > x1 else -1
            y, x = y1 + step_y, x1 + step_x
            while y != y2 and x != x2:
                if board[y][x] is not None:
                    print("Error: path is blocked")
                    return False
                y += step_y
                x += step_x
        else:
            print("Error: Queen moves only straight or diagonal")
            return False

        target = board[y2][x2]
        if target is None or target.color != self.color:
            board[y2][x2] = board[y1][x1]
            board[y1][x1] = None
            return True
        else:
            print("Error: Cannot capture own piece")
            return False

class Bishop(Piece):
    def symbol(self):
        return "wB" if self.color == "white" else "bB"
    
    def move(self, board, from_pos, to_pos):
        y1, x1 = from_pos
        y2, x2 = to_pos

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        if dx != dy:
            print("Error: Bishop must move diagonally")
            return False

        step_y = 1 if y2 > y1 else -1
        step_x = 1 if x2 > x1 else -1

        y, x = y1 + step_y, x1 + step_x
        while y != y2 and x != x2:
            if board[y][x] is not None:
                print("Error: path is blocked")
                return False
            y += step_y
            x += step_x

        target = board[y2][x2]
        if target is None or target.color != self.color:
            board[y2][x2] = board[y1][x1]
            board[y1][x1] = None
            return True
        else:
            print("Error: Cannot capture own piece")
            return False


class Knight(Piece):
    def symbol(self):
        return "wN" if self.color == "white" else "bN"
    
    def move(self, board, from_pos, to_pos):
        y1, x1 = from_pos
        y2, x2 = to_pos

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        if (dx == 2 and dy == 1) or (dx == 1 and dy == 2):
            target = board[y2][x2]
            if target is None or target.color != self.color:
                board[y2][x2] = board[y1][x1]
                board[y1][x1] = None
                return True
            else:
                print("Error: Cannot capture own piece")
                return False
        else:
            print("Error: Invalid knight move")
            return False



def user_to_matrix(pos):
    # a1 = (7, 0)
    x, y = list(pos)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    return 8-int(y), letters.index(x)

def main():
    board = Board()
    board.setup()
    turn = "white"  # White starts

    while True:
        board.show_board()
        print(f"{turn.capitalize()}'s turn.")

        user_from = input("Enter figure's position e.g. a1 (or 'quit' to exit): ")
        if user_from.lower() == "quit":
            break

        user_to = input("Enter where to move e.g. a5: ")

        from_pos = user_to_matrix(user_from)
        to_pos = user_to_matrix(user_to)

        piece = board.board[from_pos[0]][from_pos[1]]
        if piece is None:
            print("There is no piece at that position. Try again.")
            continue

        if piece.color != turn:
            print(f"It's {turn}'s turn. You cannot move {piece.color}'s piece.")
            continue

        moved = piece.move(board.board, from_pos, to_pos)
        if moved:
            turn = "black" if turn == "white" else "white"
        else:
            print("Invalid move. Try again.")

main()
