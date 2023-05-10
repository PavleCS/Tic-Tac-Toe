import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple


class Board(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic Tac Toe Game")
        self.cells = {}
        self.game = game
        self.create_menu()
        self.create_board()
        self.create_grid()

    def create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(
            label="Play Again",
            command=self.reset_board
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def create_board(self):
        display_frame = tk.Frame(master=self, bg="#F9FBE7", pady=5, padx=5)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
            fg="#FEA1A1",
            bg="#F9FBE7"
        )
        self.display.pack()

    def create_grid(self):
        grid_frame = tk.Frame(master=self, bg="#F9FBE7", padx=5, pady=5)
        grid_frame.pack()
        # self.button_image = tk.PhotoImage(file="btn.png")
        # self.button_image = self.button_image.subsample(2, 2)
        for row in range(self.game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self.game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    font=font.Font(size=36, weight="bold"),
                    # image=self.button_image,
                    highlightthickness=0,
                    bg="#F0EDD4",
                    border=0,
                    text="",
                    width=3,
                    height=1,
                )
                self.cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="snew"
                )

    def play(self, event):
        clicked_btn = event.widget
        row, col = self.cells[clicked_btn]
        move = Move(row, col, self.game.current_player.label)
        if self.game.is_valid_move(move):
            self.update_button(clicked_btn)
            self.game.process_move(move)
            if self.game.is_tied():
                self.update_display(msg="Tied game!", color="red")
            elif self.game.has_winner:
                self.highlight_cells()
                msg = f'Player "{self.game.current_player.label}" won!'
                color = self.game.current_player.color
                self.update_display(msg, color)
            else:
                self.game.toggle_player()
                msg = f"{self.game.current_player.label}'s turn"
                self.update_display(msg)

    def update_button(self, clicked_btn):
        clicked_btn.config(text=self.game.current_player.label)
        clicked_btn.config(fg=self.game.current_player.color)

    def update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def highlight_cells(self):
        for button, coordinates in self.cells.items():
            if coordinates in self.game.winner_combo:
                button.config(highlightbackground="red")

    def reset_board(self):
        self.game.reset_game()
        self.update_display(msg="Ready?")
        for button in self.cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")


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


class GameLogic:
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

    def is_tied(self):
        no_winner = not self.has_winner
        played_moves = (
            move.label for row in self.current_moves for move in row
        )
        return no_winner and all(played_moves)

    def toggle_player(self):
        self.current_player = next(self.players)

    def reset_game(self):
        for row, row_content in enumerate(self.current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []


def main():
    game = GameLogic()
    board = Board(game)
    board.mainloop()


if __name__ == "__main__":
    main()
