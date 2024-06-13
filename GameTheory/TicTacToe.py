import tkinter as tk
from tkinter import messagebox
import math
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe with Minimax")
        self.window.minsize(300, 350)
        self.buttons = [None] * 9
        self.initialize_board()
        self.first_move()
        self.game_over = False

        # Restart button
        self.restart_button = tk.Button(self.window, text="Restart", font="Arial 20", height=1, width=6, bg="sky blue",
                                        command=self.restart_game)
        self.restart_button.grid(row=3, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.mainloop()

    def initialize_board(self):
        self.board = [" " for _ in range(9)]  #For the board as a

        # Adjustments for the buttons
        button_font = "Arial 30 bold"
        button_height = 2
        button_width = 6
        button_bg = "white"
        button_active_bg = "dark grey"

        for i in range(9):
            if self.buttons[i] is None:
                button = tk.Button(self.window, text="", font=button_font, height=button_height, width=button_width, bg=button_bg,
                                   activebackground=button_active_bg,
                                   command=lambda i=i: self.on_button_click(i))
                button.grid(row=i // 3, column=i % 3, padx=3, pady=3)
                self.buttons[i] = button
            else:
                self.buttons[i].config(text="", state="normal", bg=button_bg)

    def first_move(self):
        self.current_player = "O"
        self.ai_move(True)

    def on_button_click(self, i):
        if self.board[i] == " " and not self.game_over:
            self.make_move(i,self.current_player)

            if not self.game_over:
                self.current_player = "O"
                self.ai_move()

    def make_move(self, i, player):
        self.board[i] = player
        if player == "X":
            self.buttons[i].configure(text=player, fg="blue")
        else:
            self.buttons[i].configure(text=player, fg="green")

        # Check for win or draw and disable buttons if game is over
        if self.check_winner(player):
            messagebox.showinfo("Game Over", f"Player {player} wins!")
            self.disable_buttons()
            self.game_over = True
        elif self.check_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.disable_buttons()
            self.game_over = True

    def ai_move(self, is_first=False):
        if is_first:
            random_place = random.randint(0,8)
            self.make_move(random_place, self.current_player)
        else:
            best_score = -math.inf
            best_move = None

            for i in range(len(self.board)):
                if self.board[i] == " ":
                    self.board[i] = self.current_player
                    score = self.minimax(self.board, 0, False)
                    self.board[i] = " "
                    if score > best_score:
                        best_score = score
                        best_move = i

            self.make_move(best_move, self.current_player)
        self.current_player = "X" if self.current_player == "O" else "O"  # Switch players

    def minimax(self, board, depth, is_maximizing, alpha=-math.inf, beta=math.inf):
        result = self.check_terminal()
        if result is not None:
            return result

        if is_maximizing:
            best_score = -math.inf
            for i in range(len(board)):
                if board[i] == " ":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False, alpha, beta)
                    board[i] = " "
                    best_score = max(score, best_score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
            return best_score
        else:
            best_score = math.inf
            for i in range(len(board)):
                if board[i] == " ":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True, alpha, beta)
                    board[i] = " "
                    best_score = min(score, best_score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
            return best_score

    def check_winner(self, player):
        win_states = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for state in win_states:
            if all(self.board[i] == player for i in state):
                return True
        return False

    def check_draw(self):
        return all(cell != " " for cell in self.board)

    def check_terminal(self):
        if self.check_winner("X"):
            return -1
        if self.check_winner("O"):
            return 1
        if self.check_draw():
            return False
        return None

    def restart_game(self):
        self.game_over = False
        self.initialize_board()
        self.first_move()

    def disable_buttons(self):
        for button in self.buttons:
            button.config(state="disabled")

    def on_close(self):
        self.game_over = True
        self.window.destroy()

# Start the game
if __name__ == "__main__":
    TicTacToe()