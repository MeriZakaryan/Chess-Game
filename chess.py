#!/usr/bin/env python3

class Piece:
    def __init__(self, color):
        self.color = color
    
    # from_pos = (x1, y1) is tuple then to_pos = (x2, y2)
    # x is like OX (a, b, c, d, e, f, g, h)
    # y is like OY (1, 2, 3, 4, 5, 6, 7, 8) 
    def capture_move(self, board, from_pos, to_pos):
        y1, x1 = from_pos
        y2, x2 = to_pos
        target = board[y2][x2]
        if target is None or target.color != self.color:
            board[y2][x2] = board[y1][x1]
            board[y1][x1] = None
            return True
        else:
            print("Error: Cannot capture own piece")
            return False

class Board:
    def __init__(self):
        self.board = []
        for i in range(8):
            row = []
            for cell in range(8):
                row.append(None)
            self.board.append(row)
    
    def is_empty(self, y, x):
        return self.board[y][x] is None
    
    def setup(self):
        figures = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for x, figure in enumerate(figures):
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
            print()
        print("  a  b  c  d  e  f  g  h")

class CheckMate:
    def __init__(self, board):
        self.board = board.board
    
    def find_king(self, color):
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if isinstance(piece, King) and piece.color == color:
                    return (y, x)
        return None
    
    def is_in_check(self, color):
        king_pos = self.find_king(color)
        if king_pos is None:
            return False
        opponent_color = "black" if color == "white" else "white"
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece is not None and piece.color == opponent_color:
                    if self.can_piece_attack(piece, king_pos):
                        return True
        return False

    def can_piece_attack(self, piece, king_pos):
        for y in range(8):  # Iterate over all rows again
            for x in range(8):  # Iterate over all columns
                if piece and piece.color != self.board[king_pos[0]][king_pos[1]].color:
                    # Save original pieces for undoing move later
                    original_target = self.board[king_pos[0]][king_pos[1]]  # Piece at king's square
                    original_piece = self.board[y][x]  # The attacking piece itself

                    if piece.move(self.board, (y, x), king_pos):
                        # Undo the move to keep self.board unchanged
                        self.board[y][x] = original_piece
                        self.board[king_pos[0]][king_pos[1]] = original_target
                        return True  # King is under attack (in check)
        return False
    
    

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False

    def symbol(self):
        return "wR" if self.color == "white" else "bR"
    
    def move(self, board, from_pos, to_pos):
        y1, x1 = from_pos
        y2, x2 = to_pos

        if x1 == x2:  # Vertical 
            step = 1 if y1 < y2 else -1
            for y in range(y1 + step, y2, step):
                if board[y][x1] is not None:
                    print("Error: Path is blocked")
                    return False
        elif y1 == y2:  # Horizontal 
            step = 1 if x1 < x2 else -1
            for x in range(x1 + step, x2, step):
                if board[y1][x] is not None:
                    print("Error: Path is blocked")
                    return False
        else:
            print("Error: Rook must move horizontally or vertically")
            return False
        
        can_move = self.capture_move(board, from_pos, to_pos) #there are not any obstacles, so it can move
        if can_move:
            self.has_moved = True
                
        return can_move



class Pawn(Piece):
    def symbol(self):
        return "wP" if self.color == "white" else "bP"
    
    def move(self, board, from_pos, to_pos):
        y1, x1 = from_pos
        y2, x2 = to_pos

        step = -1 if self.color == "white" else 1  

        if x2 == x1 and y2 == y1 + step:
            if board[y2][x2] is None:
                board[y2][x2] = board[y1][x1]
                board[y1][x1] = None
                return True
            else:
                print("Error: Cannot move forward, square occupied")
                return False

        start_row = 6 if self.color == "white" else 1
        if x2 == x1 and y1 == start_row and y2 == y1 + 2*step:
            if board[y1 + step][x1] is None and board[y2][x2] is None:
                board[y2][x2] = board[y1][x1]
                board[y1][x1] = None
                return True
            else:
                print("Error: Cannot move two squares, path blocked")
                return False

        # Eat dioganally
        if abs(x2 - x1) == 1 and y2 == y1 + step:
            target = board[y2][x2]
            if target is not None and target.color != self.color:
                board[y2][x2] = board[y1][x1]
                board[y1][x1] = None
                return True
            else:
                print("Error: Cannot capture - no enemy piece or square empty")
                return False

        print("Error: Invalid pawn move")
        return False    


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False

    def symbol(self):
        return "wK" if self.color == "white" else "bK"
    
    def castling(self, board, from_pos, to_pos):
        y, x1 = from_pos
        x2 = to_pos[1] # y is the same 

        if x2 == x1 - 2: # queen side
            rook_pos = (y, 0)
            path = [(y, x1-1), (y, x1-2)]
        else:
            rook_pos = (y, 7)
            path = [(y, x1+1), (y, x1+2)]

        rook = board[rook_pos[0]][rook_pos[1]]
        if not isinstance(rook, Rook) or rook.color != self.color or self.has_moved or rook.has_moved:
            print("Error: Can not do castling")
            return False

        for cell in path:
            if board[cell[0]][cell[1]] is not None:
                print("Castling path is blocked")
                return False
            
        board[y][x2] = self
        board[y][x1] = None
        if x2 < x1: # queen side
            board[y][x2 + 1] = rook
            board[rook_pos[0]][rook_pos[1]] = None
        else: #king side
            board[y][x2 - 1] = rook
            board[rook_pos[0]][rook_pos[1]] = None

        self.has_moved = True
        rook.has_moved = True
        return True

    def move(self, board, from_pos, to_pos):
        y1, x1 = from_pos
        y2, x2 = to_pos
        
        if abs(x2 - x1) <= 1 and abs(y2 - y1) <= 1:
            if y1 == y2 and x1 == x2:
                print("Error: King must move to a different square")
                return False
            
            opponent_color = "black" if self.color == "white" else "white"
            for row in range(8):
                for col in range(8):
                    piece = board[row][col]
                    if (piece is not None and 
                        isinstance(piece, King) and 
                        piece.color == opponent_color):
                        
                        if abs(y2 - row) <= 1 and abs(x2 - col) <= 1:
                            print("Error: King cannot move adjacent to opponent's king")
                            return False
                        break 

            can_move = self.capture_move(board, from_pos, to_pos) #there are not any obstacles, so it can move
            if can_move:
                self.has_moved = True

            return can_move
        elif y1 == y2 and abs(x2 - x1) == 2:
            return self.castling(board, from_pos, to_pos)
        else:
            print("Error: King can only move 1 square in any direction")
            return False


class Bishop(Piece):
    def symbol(self):
        return "wB" if self.color == "white" else "bB"
    
    def move(self, board, from_pos, to_pos):
        y1, x1 = from_pos
        y2, x2 = to_pos

        if abs(x2 - x1) != abs(y2 - y1):
            print("Error: Bishop must move diagonally")
            return False

        step_y = 1 if y2 > y1 else -1
        step_x = 1 if x2 > x1 else -1

        y, x = y1 + step_y, x1 + step_x
        while y != y2 and x != x2:
            if board[y][x] is not None:
                print("Error: Path is blocked")
                return False
            y += step_y
            x += step_x

        return self.capture_move(board, from_pos, to_pos)

class Queen(Piece):
    def symbol(self):
        return "wQ" if self.color == "white" else "bQ"
    
    def move(self, board, from_pos, to_pos):
        y1, x1 = from_pos
        y2, x2 = to_pos
        
        if x1 == x2: 
            step = 1 if y1 < y2 else -1
            for y in range(y1 + step, y2, step):
                if board[y][x1] is not None:
                    print("Error: Path is blocked")
                    return False
        elif y1 == y2:  
            step = 1 if x1 < x2 else -1
            for x in range(x1 + step, x2, step):
                if board[y1][x] is not None:
                    print("Error: Path is blocked")
                    return False
        elif abs(x2 - x1) == abs(y2 - y1): 
            step_y = 1 if y2 > y1 else -1
            step_x = 1 if x2 > x1 else -1
            y, x = y1 + step_y, x1 + step_x
            while y != y2 and x != x2:
                if board[y][x] is not None:
                    print("Error: Path is blocked")
                    return False
                y += step_y
                x += step_x
        else:
            print("Error: Queen can only move horizontally, vertically, or diagonally")
            return False

        return self.capture_move(board, from_pos, to_pos)


class Knight(Piece):
    def symbol(self):
        return "wN" if self.color == "white" else "bN"
    
    def move(self, board, from_pos, to_pos):
        y1, x1 = from_pos
        y2, x2 = to_pos

        if (abs(x2 - x1) == 2 and abs(y2 - y1) == 1) or (abs(x2 - x1) == 1 and abs(y2 - y1) == 2):
            return self.capture_move(board, from_pos, to_pos)
        else:
            print("Error: Knight must move in L-shape (2+1 squares)")
            return False


def user_to_matrix(pos):
    if len(pos) != 2:
        return None
    
    x, y = list(pos.lower())
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    
    if x not in letters or y not in '12345678':
        return None
    
    return 8 - int(y), letters.index(x)  


def is_valid_position(pos):
    if len(pos) != 2:
        return False
    x, y = pos.lower()
    return x in 'abcdefgh' and y in '12345678'


def main():
    board = Board()
    board.setup()
    rules = CheckMate(board)
    turn = "white" 

    print("Welcome to Chess!")
    print("Enter moves in chess notation (e.g., 'e2' to 'e4')")
    print("Type 'quit' to exit the game\n")

    while True:
        board.show_board()
        print(f"\n{turn.capitalize()}'s turn.")

        user_from = input("Enter piece position (e.g., e2): ").strip()
        if user_from.lower() == "quit":
            print("Thanks for playing!")
            break

        if not is_valid_position(user_from):
            print("Invalid position format. Use format like 'e2'")
            continue

        user_to = input("Enter destination (e.g., e4): ").strip()
        if not is_valid_position(user_to):
            print("Invalid position format. Use format like 'e4'")
            continue

        from_pos = user_to_matrix(user_from)
        to_pos = user_to_matrix(user_to)

        piece = board.board[from_pos[0]][from_pos[1]]
        if piece is None:
            print("No piece at that position. Try again.")
            continue

        if piece.color != turn:
            print(f"It's {turn}'s turn. You cannot move {piece.color}'s piece.")
            continue

        if not (0 <= to_pos[0] < 8 and 0 <= to_pos[1] < 8):
            print("Move is outside the board.")
            continue

        if piece.move(board.board, from_pos, to_pos):
            turn = "black" if turn == "white" else "white"
            if rules.is_in_check(turn):
                print(f"Warning! {turn.capitalize()} is in check!")
        else:
            print("Invalid move. Try again.")

        print() 


if __name__ == "__main__":
    main()