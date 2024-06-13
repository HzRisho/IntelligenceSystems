import tkinter as tk
from tkinter import messagebox
import math
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        
        # Set a fixed window size.
        self.window.geometry("300x350")  # Width = 3*100 (for buttons) + 6 (for grid lines), Height includes restart button and window title.
        self.window.resizable(False, False)
        
        self.initialize_game_state()
        self.initialize_board()
        self.window.mainloop()

    def initialize_game_state(self):
        # Initialize game state variables
        self.current_player = "O"
        self.board = [" "] * 9
        self.game_over = False
        self.buttons = []
        self.First_Move = True

    def initialize_board(self):
        button_size = 100  # Size in pixels for each button
        for i in range(9):
            frame = tk.Frame(self.window, width=button_size, height=button_size)
            frame.grid(row=i // 3, column=i % 3)
            frame.pack_propagate(False)  # Prevent the frame from resizing to fit the button
            button = tk.Button(frame, text='', font="Arial 20", command=lambda i=i: self.on_button_click(i))
            button.pack(expand=True, fill='both')  # Make the button fill the frame
            self.buttons.append(button)

        # Restart button
        self.restart_button = tk.Button(self.window, text="Restart", font="Arial 20", command=self.restart_game)
        self.restart_button.grid(row=3, column=0, columnspan=3, sticky="ew")

        if self.current_player == "O":
            self.ai_move()

    def on_button_click(self, i):
        # Make a move for human player and then for AI.
        if self.board[i] == " " and not self.game_over:
            self.make_move(i, "X")
            if not self.game_over:
                self.ai_move()

    def make_move(self, i, player):
        # Place the player's symbol on the board and check for end game.
        self.board[i] = player
        self.buttons[i].config(text=player)
        self.check_end_game(player)

    def ai_move(self):
        # If it's the first move of the AI, choose a random position
        if self.First_Move:
            self.First_Move = False
            empty_indices = [i for i, x in enumerate(self.board) if x == " "]
            random_place = random.choice(empty_indices)
            self.make_move(random_place, "O")
        else:
            # AI performs a move using the minimax algorithm with alpha-beta pruning.
            best_score = -float('inf')
            best_move = None
            for i in range(9):
                if self.board[i] == " ":
                    self.board[i] = "O"
                    score = self.minimax(0, False, -float('inf'), float('inf'))
                    self.board[i] = " "
                    if score > best_score:
                        best_score = score
                        best_move = i
            if best_move is not None:
                self.make_move(best_move, "O")

    def minimax(self, depth, is_maximizing, alpha, beta):
        # Minimax algorithm with alpha-beta pruning and depth control.
        if self.check_winner("O"):
            return 1
        if self.check_winner("X"):
            return -1
        if all(space != " " for space in self.board):
            return 0

        if depth == 4:  # Limit the depth to 4 recursive calls to save computation time.
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if self.board[i] == " ":
                    self.board[i] = "O"
                    score = self.minimax(depth + 1, False, alpha, beta)
                    self.board[i] = " "
                    best_score = max(best_score, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if self.board[i] == " ":
                    self.board[i] = "X"
                    score = self.minimax(depth + 1, True, alpha, beta)
                    self.board[i] = " "
                    best_score = min(best_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
            return best_score

    def check_winner(self, player):
        # Check if the player has won.
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6)]
        for condition in win_conditions:
            if all(self.board[i] == player for i in condition):
                return True
        return False

    def check_end_game(self, player):
        # Check for a win or draw and announce the game's end.
        if self.check_winner(player):
            messagebox.showinfo("Game Over", f"Player {player} wins!")
            self.game_over = True
        elif all(space != " " for space in self.board):
            messagebox.showinfo("Game Over", "It's a draw!")
            self.game_over = True

    def restart_game(self):
        # Reset the game state to start a new game.
        self.board = [" "] * 9
        for button in self.buttons:
            button.config(text="", state="normal")
        self.current_player = "O"
        self.game_over = False
        self.First_Move = True  # Reset this flag for the new game
        self.ai_move()

if __name__ == "__main__":
    TicTacToe()
