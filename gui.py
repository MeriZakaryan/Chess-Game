import tkinter as tk
from PIL import Image, ImageTk
import chess  # your updated chess.py

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game")
        self.size = 768
        self.square = self.size // 8

        self.canvas = tk.Canvas(root, width=self.size, height=self.size)
        self.canvas.pack()

        self.message = tk.Label(root, text="", font=("Arial", 14), fg="red")
        self.message.pack()

        # Load board image
        board_img = Image.open("assets/board.png").resize((self.size, self.size), Image.Resampling.LANCZOS)
        self.board_photo = ImageTk.PhotoImage(board_img)
        self.canvas.create_image(0, 0, image=self.board_photo, anchor="nw")

        # Load piece images
        names = ['wR','wN','wB','wQ','wK','wP','bR','bN','bB','bQ','bK','bP']
        self.pieces = {
            name: ImageTk.PhotoImage(
                Image.open(f"assets/{name}.png").resize((self.square, self.square), Image.Resampling.LANCZOS)
            ) for name in names
        }

        # Game logic
        self.board = chess.Board()
        self.board.setup()
        self.rules = chess.CheckMate(self.board)
        self.turn = "white"
        self.selected = None

        self.canvas.bind("<Button-1>", self.on_click)
        self.redraw()

    def redraw(self):
        self.canvas.delete("piece")
        for r in range(8):
            for c in range(8):
                piece = self.board.board[r][c]
                if piece:
                    x, y = c * self.square, r * self.square
                    symbol = piece.symbol()
                    self.canvas.create_image(x, y, image=self.pieces[symbol], anchor="nw", tags="piece")
#   1.	Clears the canvas.
#	2.	Draws the board image again.
#	3.	Draws all pieces in their new positions.


    def show_message(self, text, color="red", duration=2000):
        self.message.config(text=text, fg=color)
        self.root.after(duration, lambda: self.message.config(text=""))

    def highlight_selected_piece(self, r, c):
        x, y = c * self.square, r * self.square
        self.canvas.create_rectangle(
            x, y, x + self.square, y + self.square,
            outline="#0000FF", width=3, tags="highlight"
        )

    def on_click(self, event):
        r, c = event.y // self.square, event.x // self.square

        if self.selected is None:
            piece = self.board.board[r][c]
            if piece and piece.color == self.turn:
                self.selected = (r, c)
                self.canvas.delete("highlight")
                self.highlight_selected_piece(r, c)
            else:
                self.show_message("Select your own piece!")
        else:
            from_pos = self.selected
            to_pos = (r, c)
            piece = self.board.board[from_pos[0]][from_pos[1]]

            if self.rules.is_legal_move(piece, from_pos, to_pos): #is this move allowed for this piece?
                moved = False
                if isinstance(piece, chess.King):
                    moved = piece.move(self.board.board, from_pos, to_pos, rules=self.rules)
                else:
                    moved = piece.move(self.board.board, from_pos, to_pos)

                if moved:
                    self.redraw()
                    if self.rules.is_in_check(self.turn):
                        self.show_message("You are still in check!", "orange")

                    opponent = "black" if self.turn == "white" else "white"
                    if self.rules.is_in_check(opponent):
                        if not self.rules.has_legal_moves(opponent):
                            self.show_message(f"Checkmate! {self.turn.capitalize()} wins!", "green", duration=5000)
                            self.canvas.unbind("<Button-1>")
                        else: 
                            self.show_message(f"{opponent.capitalize()} is in check!", "orange")

                    elif not self.rules.has_legal_moves(opponent):
                        self.show_message("Stalemate! It's a draw!", "blue", duration=5000)
                        self.canvas.unbind("<Button-1>")

                    self.turn = opponent
                else:
                    self.show_message("Invalid move.")
            else:
                self.show_message("Illegal move.")

            self.selected = None
            self.canvas.delete("highlight")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessGUI(root)
    root.mainloop()


#to do
# self.turn = opponent
#error handleing is also used in chess.py
