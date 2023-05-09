import tkinter as tk
from tkinter import font


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
