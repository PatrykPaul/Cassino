import tkinter as tk
from tkinter import messagebox
import random

WIDTH, HEIGHT = 18, 14
MINES = 40

class Minesweeper(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Saper")
        self.board = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.remaining_tiles = WIDTH * HEIGHT
        self.marked_mines = 0
        self.create_widgets()

    def create_widgets(self):
        self.remaining_mines_frame = tk.Frame(self)
        self.remaining_mines_frame.grid(row=0, column=0, columnspan=WIDTH)

        self.remaining_mines_label = tk.Label(self.remaining_mines_frame, text="Miny: " + str(MINES))
        self.remaining_mines_label.pack()

        self.buttons = [[tk.Button(self, width=2, height=1, command=lambda x=x, y=y: self.click(x, y)) for x in range(WIDTH)] for y in range(HEIGHT)]
        for y in range(HEIGHT):
            for x in range(WIDTH):
                self.buttons[y][x].grid(row=y+1, column=x)

        for y in range(HEIGHT):
            for x in range(WIDTH):
                self.buttons[y][x].bind("<Button-3>", lambda event, x=x, y=y: self.mark_mine(x, y))

        self.generate_mines()

    def generate_mines(self):
        mines_generated = 0
        while mines_generated < MINES:
            x, y = random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1)
            if self.board[y][x] != -1:
                self.board[y][x] = -1
                mines_generated += 1

    def click(self, x, y):
        if self.board[y][x] == -1:
            self.buttons[y][x].config(text="X", state="disabled")
            messagebox.showinfo("Game Over", "You clicked on a mine! Game Over!")
            self.destroy()
        else:
            mines_count = self.count_adjacent_mines(x, y)
            self.buttons[y][x].config(text=str(mines_count), state="disabled")
            self.remaining_tiles -= 1
            if mines_count == 0:
                self.expand_empty(x, y)
            if self.remaining_tiles == MINES:
                messagebox.showinfo("Congratulations", "You have won the game!")

    def count_adjacent_mines(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if 0 <= x+dx < WIDTH and 0 <= y+dy < HEIGHT:
                    if self.board[y+dy][x+dx] == -1:
                        count += 1
        return count

    def expand_empty(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if 0 <= x+dx < WIDTH and 0 <= y+dy < HEIGHT:
                    if self.buttons[y+dy][x+dx]["state"] == "normal":
                        mines_count = self.count_adjacent_mines(x+dx, y+dy)
                        self.buttons[y+dy][x+dx].config(text=str(mines_count), state="disabled")
                        self.remaining_tiles -= 1
                        if mines_count == 0:
                            self.expand_empty(x+dx, y+dy)

    def mark_mine(self, x, y):
        if self.buttons[y][x]["text"] == "":
            self.buttons[y][x].config(text="X", state="disabled")
            self.marked_mines += 1
        elif self.buttons[y][x]["text"] == "X":
            self.buttons[y][x].config(text="", state="normal")
            self.marked_mines -= 1


        remaining_mines = MINES - self.marked_mines
        self.remaining_mines_label.config(text="Remaining Mines: " + str(remaining_mines))

if __name__ == "__main__":
    app = Minesweeper()
    app.mainloop()