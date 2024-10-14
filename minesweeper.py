import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")
        self.size = 50
        self.mines = 400
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.flags = [[False for _ in range(self.size)] for _ in range(self.size)]
        self.game_over = False
        self.first_click = True

        self.create_widgets()
        self.create_grid()

    def create_widgets(self):
        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        self.game_frame = tk.Frame(self.master)
        self.game_frame.pack()

        self.mines_left = tk.Label(self.top_frame, text=f"Mines left: {self.mines}")
        self.mines_left.pack(side=tk.LEFT, padx=5, pady=5)

        self.new_game_button = tk.Button(self.top_frame, text="New Game", command=self.new_game)
        self.new_game_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def create_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                btn = tk.Button(self.game_frame, width=2, height=1)
                btn.grid(row=i, column=j)
                btn.bind('<Button-1>', lambda e, row=i, col=j: self.left_click(row, col))
                btn.bind('<Button-3>', lambda e, row=i, col=j: self.right_click(row, col))
                self.buttons[i][j] = btn

    def place_mines(self, first_row, first_col):
        positions = [(r, c) for r in range(self.size) for c in range(self.size) if (r, c) != (first_row, first_col)]
        mine_positions = random.sample(positions, self.mines)

        for r, c in mine_positions:
            self.grid[r][c] = -1
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size and self.grid[nr][nc] != -1:
                        self.grid[nr][nc] += 1

    def left_click(self, row, col):
        if self.game_over:
            return

        if self.first_click:
            self.place_mines(row, col)
            self.first_click = False

        if self.flags[row][col]:
            return

        if self.grid[row][col] == -1:
            self.game_over = True
            self.reveal_all()
            messagebox.showinfo("Game Over", "You hit a mine!")
        else:
            self.reveal(row, col)

        if self.check_win():
            self.game_over = True
            messagebox.showinfo("Congratulations", "You win!")

    def right_click(self, row, col):
        if self.game_over or self.buttons[row][col]['state'] == 'disabled':
            return

        if self.flags[row][col]:
            self.flags[row][col] = False
            self.buttons[row][col].config(text="")
            self.mines += 1
        else:
            self.flags[row][col] = True
            self.buttons[row][col].config(text="🚩")
            self.mines -= 1

        self.mines_left.config(text=f"Mines left: {self.mines}")

    def reveal(self, row, col):
        if self.buttons[row][col]['state'] == 'disabled':
            return

        self.buttons[row][col].config(state='disabled')

        if self.grid[row][col] > 0:
            self.buttons[row][col].config(text=str(self.grid[row][col]))
        elif self.grid[row][col] == 0:
            self.buttons[row][col].config(relief=tk.SUNKEN)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size:
                        self.reveal(nr, nc)

    def reveal_all(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == -1:
                    self.buttons[i][j].config(text="💣", state='disabled')
                elif self.grid[i][j] > 0:
                    self.buttons[i][j].config(text=str(self.grid[i][j]), state='disabled')
                else:
                    self.buttons[i][j].config(relief=tk.SUNKEN, state='disabled')

    def check_win(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] != -1 and self.buttons[i][j]['state'] != 'disabled':
                    return False
        return True

    def new_game(self):
        self.master.destroy()
        root = tk.Tk()
        Minesweeper(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()