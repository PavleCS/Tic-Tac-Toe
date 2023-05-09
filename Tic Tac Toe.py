import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple


class Board(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe Game")
        self.cells = {}
        self.create_board()
        self.create_grid()

    def create_board(self):
        display_frame = tk.Frame(master=self, bg="#F6F1F1")
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
            fg="#19A7CE",
            bg="#F6F1F1"
        )
        self.display.pack()

    def create_grid(self):
        grid_frame = tk.Frame(master=self, bg="#F6F1F1")
        grid_frame.pack()
        self.button_image = tk.PhotoImage(file="btn.png")
        self.button_image = self.button_image.subsample(2, 2)
        for row in range(3):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(3):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    image=self.button_image,
                    highlightthickness=0,
                    bg="#F6F1F1",
                    border=0,
                    width=100,
                    height=100,
                )
                self.cells[button] = (row, col)
                button.grid(
                    row=row,
                    column=col,
                    padx=3,
                    pady=3,
                    sticky="snew"
                )


class Player(NamedTuple):
    label: str
    color: str


class Move(NamedTuple):
    row: int
    col: int
    label: str = ""


BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="blue"),
    Player(label='O', color="green"),
)


class Game:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self.players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self.players)
        self.winner_combo = []
        self.current_moves = []
        self.has_winner = False
        self.winning_combos = []
        self.setup_board()

    def setup_board(self):
        self.current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self.winning_combos = self.get_winning_combos()

    def get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self.current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def is_valid_move(self, move):
        row, col = move.row, move.col
        move_was_not_played = self.current_moves[row][col].label == ""
        no_winner = not self.has_winner
        return no_winner and move_was_not_played

    def process_move(self, move):
        row, col = move.row, move.col
        self.current_moves[row][col] = move
        for combo in self.winning_combos:
            results = set(
                self.current_moves[n][m].label
                for n, m in combo
            )
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                self.has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        return self.has_winner


def main():
    board = Board()
    board.mainloop()


if __name__ == "__main__":
    main()
