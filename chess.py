#!/usr/bin/env python3

class Piece:
    def __init__(self, color):
        self.color = color
    # from_pos = (y, x) is tuple then to_pos = (y, x)
    # x is like OX (a, b, c, d, e, f, g, h) 
    # y is like OY (8, 7, 6, 5, 4, 3, 2, 1) 
    def capture_move(self, board, from_pos, to_pos):
        y1, x1 = from_pos
        y2, x2 = to_pos
        target = board[y2][x2]
        if target is None or target.color != self.color:
            board[y2][x2] = board[y1][x1]
            board[y1][x1] = None
            return True
        else:
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
        
        # Checking if any opponent piece can attack the king
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece is not None and piece.color == opponent_color:
                    if self.can_piece_attack(piece, (y, x), king_pos):
                        return True
        return False

    def can_piece_attack(self, piece, piece_pos, target_pos):
        # Testing if piece at piece_pos can attack target_pos
        # This is a copy of the board state to test the move
        original_target = self.board[target_pos[0]][target_pos[1]]
        original_piece = self.board[piece_pos[0]][piece_pos[1]]
        
        if isinstance(piece, King):
            y1, x1 = piece_pos
            y2, x2 = target_pos
            # King can attack if it's within one square (but we don't check for check here)
            if abs(y2 - y1) <= 1 and abs(x2 - x1) <= 1 and not (y1 == y2 and x1 == x2):
                return True
            return False
        elif isinstance(piece, Pawn):
            # Pawn diagonal attack 
            y1, x1 = piece_pos
            y2, x2 = target_pos
            step = -1 if piece.color == "white" else 1
            if abs(x2 - x1) == 1 and y2 == y1 + step:
                return True
            return False
        else:
            result = piece.move(self.board, piece_pos, target_pos)
            # Restore the board state
            self.board[piece_pos[0]][piece_pos[1]] = original_piece
            self.board[target_pos[0]][target_pos[1]] = original_target
            return result
    
    def has_legal_moves(self, color):
        for y1 in range(8): 
            for x1 in range(8):  
                piece = self.board[y1][x1]  
                if piece and piece.color == color:  
                    for y2 in range(8): 
                        for x2 in range(8):  
                            if self.is_legal_move(piece, (y1, x1), (y2, x2)):
                                return True
        return False

    def is_legal_move(self, piece, from_pos, to_pos):
        # Test if a move is legal (doesn't leave king in check)
        original_target = self.board[to_pos[0]][to_pos[1]]
        original_piece = self.board[from_pos[0]][from_pos[1]]
        
        move_successful = False
        if isinstance(piece, King):
            if abs(to_pos[1] - from_pos[1]) == 2:
                move_successful = piece.castling(self.board, from_pos, to_pos, rules=self, simulate=True)
            else:
                move_successful = piece.move(self.board, from_pos, to_pos, rules=self)
        else:
            move_successful = piece.move(self.board, from_pos, to_pos)
            
        if move_successful:
            king_safe = not self.is_in_check(piece.color)
          
            self.board[from_pos[0]][from_pos[1]] = original_piece
            self.board[to_pos[0]][to_pos[1]] = original_target
            
            return king_safe
                
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

        if x1 == x2:  # Vertical movement
            step = 1 if y1 < y2 else -1
            for y in range(y1 + step, y2, step):
                if board[y][x1] is not None:
                    return False  # Path is blocked
        elif y1 == y2:  # Horizontal movement
            step = 1 if x1 < x2 else -1
            for x in range(x1 + step, x2, step):
                if board[y1][x] is not None:
                    return False  # Path is blocked
        else:
            return False  
        
        # Check if we can capture/move to destination
        can_move = self.capture_move(board, from_pos, to_pos)
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
                
                # Checking for pawn promotion
                if (self.color == "white" and y2 == 0) or (self.color == "black" and y2 == 7):
                    self.promote(board, to_pos)

                return True
            else:
                return False

        start_row = 6 if self.color == "white" else 1
        if x2 == x1 and y1 == start_row and y2 == y1 + 2*step:
            if board[y1 + step][x1] is None and board[y2][x2] is None:
                board[y2][x2] = board[y1][x1]
                board[y1][x1] = None
                return True
            else:
                return False

        # Diagonal capture
        if abs(x2 - x1) == 1 and y2 == y1 + step:
            target = board[y2][x2]
            if target is not None and target.color != self.color:
                board[y2][x2] = board[y1][x1]
                board[y1][x1] = None
                
                if (self.color == "white" and y2 == 0) or (self.color == "black" and y2 == 7):
                    self.promote(board, to_pos)

                return True
            else: 
                return False

    def promote(self, board, pos):
        print(f"Pawn reached promotion!")
        while True:
            choice = input("Choose piece for promotion (q, r, b, n): ").lower()
            if choice == "q":
                board[pos[0]][pos[1]] = Queen(self.color)
                break
            elif choice == "r":
                board[pos[0]][pos[1]] = Rook(self.color)
                break
            elif choice == "b":
                board[pos[0]][pos[1]] = Bishop(self.color)
                break
            elif choice == "n":
                board[pos[0]][pos[1]] = Knight(self.color)
                break
            else:
                print("Invalid choice. Please choose: q, r, b, or n.")


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False

    def symbol(self):
        return "wK" if self.color == "white" else "bK"
    
    def castling(self, board, from_pos, to_pos, rules=None, simulate=False):
        y, x1 = from_pos
        x2 = to_pos[1]  # y is the same 

        if x2 == x1 - 2:  # Queen side castling
            rook_pos = (y, 0)
            path = [(y, x1-1), (y, x1-2)]
            new_rook_pos = (y, x1-1)
        elif x2 == x1 + 2:  # King side castling
            rook_pos = (y, 7)
            path = [(y, x1+1), (y, x1+2)]
            new_rook_pos = (y, x1+1)
        else:
            return False

        # Checking basic castling requirements
        rook = board[rook_pos[0]][rook_pos[1]]
        if (not isinstance(rook, Rook) or 
            rook.color != self.color or 
            self.has_moved or 
            rook.has_moved):
            return False

        # Checking if path is clear
        for cell in path:
            if board[cell[0]][cell[1]] is not None:
                return False
        
        # Checking if king is currently in check or would pass through/end in check
        if rules:
            king_positions_test = [from_pos] + path  # Current, through, destination
            for pos in king_positions_test:
                # Simulating king position
                original_piece = board[pos[0]][pos[1]]
                board[pos[0]][pos[1]] = self
                if pos != from_pos:
                    board[from_pos[0]][from_pos[1]] = None

                in_check = rules.is_in_check(self.color)

                # Restore position
                board[pos[0]][pos[1]] = original_piece
                if pos != from_pos:
                    board[from_pos[0]][from_pos[1]] = self

                if in_check:
                    return False

        if simulate:
            return True     
        
        board[y][x2] = self
        board[y][x1] = None
        board[new_rook_pos[0]][new_rook_pos[1]] = rook
        board[rook_pos[0]][rook_pos[1]] = None

        self.has_moved = True
        rook.has_moved = True
        return True

    def move(self, board, from_pos, to_pos, rules=None):
        y1, x1 = from_pos
        y2, x2 = to_pos
        
        if abs(x2 - x1) <= 1 and abs(y2 - y1) <= 1:
            if y1 == y2 and x1 == x2:
                return False  
            
            if rules and rules.is_in_check(self.color):
                return False
            
            # Checking if moving next to opponent king
            opponent_color = "black" if self.color == "white" else "white"
            for row in range(8):
                for col in range(8):
                    piece = board[row][col]
                    if (piece is not None and 
                        isinstance(piece, King) and 
                        piece.color == opponent_color):
                        # Kings cannot be adjacent
                        if abs(y2 - row) <= 1 and abs(x2 - col) <= 1:
                            return False
                        break 

            can_move = self.capture_move(board, from_pos, to_pos)
            if can_move:
                self.has_moved = True

            return can_move
            
        # Castling 
        elif y1 == y2 and abs(x2 - x1) == 2:
            return self.castling(board, from_pos, to_pos, rules=rules)
        else:
            return False


class Bishop(Piece):
    def symbol(self):
        return "wB" if self.color == "white" else "bB"
    
    def move(self, board, from_pos, to_pos):
        y1, x1 = from_pos
        y2, x2 = to_pos

        if abs(x2 - x1) != abs(y2 - y1):
            return False

        step_y = 1 if y2 > y1 else -1
        step_x = 1 if x2 > x1 else -1

        y, x = y1 + step_y, x1 + step_x
        while y != y2 and x != x2:
            if board[y][x] is not None:
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
        
        # like rook
        if x1 == x2: 
            step = 1 if y1 < y2 else -1
            for y in range(y1 + step, y2, step):
                if board[y][x1] is not None:
                    return False
        elif y1 == y2:  
            step = 1 if x1 < x2 else -1
            for x in range(x1 + step, x2, step):
                if board[y1][x] is not None:
                    return False
                
        # like bishop
        elif abs(x2 - x1) == abs(y2 - y1): 
            step_y = 1 if y2 > y1 else -1
            step_x = 1 if x2 > x1 else -1
            y, x = y1 + step_y, x1 + step_x
            while y != y2 and x != x2:
                if board[y][x] is not None:
                    return False
                y += step_y
                x += step_x
        else:
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

        if rules.is_in_check(turn):
            if not rules.has_legal_moves(turn):
                opponent = "black" if turn == "white" else "white"
                print(f"Checkmate! {opponent.capitalize()} wins!")
                break
            else:
                print(f"Warning! {turn.capitalize()} is in check!")
        else:
            if not rules.has_legal_moves(turn):
                print("Stalemate! The game is a draw.")
                break

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

        if rules.is_legal_move(piece, from_pos, to_pos):
            move_success = False
            if isinstance(piece, King):
                move_success = piece.move(board.board, from_pos, to_pos, rules=rules)
            else:
                move_success = piece.move(board.board, from_pos, to_pos)
                
            if move_success:
                turn = "black" if turn == "white" else "white"
            else:
                print("Invalid move. Try again.")
        else:
            print("Invalid move. Try again.")

        print() 


if __name__ == "__main__":
    main()