import tkinter as tk
from tkinter import messagebox
import time
import random


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")
        self.root.geometry("400x500")

        # Переменные
        self.board = [""] * 9
        self.current_player = "X"
        self.game_mode = "2 players"  # "2 players" or "AI"
        self.difficulty = "Easy"  # Easy, Medium, Hard
        self.game_started = False
        self.start_time = None

        # Интерфейс
        self.create_widgets()

    def create_widgets(self):
        self.mode_label = tk.Label(self.root, text="Выберите режим игры:", font=("Arial", 14))
        self.mode_label.pack()

        self.mode_frame = tk.Frame(self.root)
        self.mode_frame.pack()

        self.two_player_button = tk.Button(
            self.mode_frame, text="2 игрока", font=("Arial", 12),
            command=lambda: self.set_mode("2 players")
        )
        self.two_player_button.grid(row=0, column=0, padx=10, pady=5)

        self.ai_button = tk.Button(
            self.mode_frame, text="Против компьютера", font=("Arial", 12),
            command=lambda: self.set_mode("AI")
        )
        self.ai_button.grid(row=0, column=1, padx=10, pady=5)

        self.difficulty_label = tk.Label(self.root, text="Выберите уровень сложности:", font=("Arial", 14))
        self.difficulty_label.pack()

        self.difficulty_frame = tk.Frame(self.root)
        self.difficulty_frame.pack()

        for i, level in enumerate(["Легкий", "Средний", "Сложный"]):
            tk.Button(
                self.difficulty_frame, text=level, font=("Arial", 12),
                command=lambda l=level: self.set_difficulty(l)
            ).grid(row=0, column=i, padx=10, pady=5)

        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        self.buttons = []
        for i in range(9):
            button = tk.Button(
                self.board_frame, text="", font=("Arial", 20), width=5, height=2,
                command=lambda i =i: self.make_move(i)
            )
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

        self.info_label = tk.Label(self.root, text="Текущий ход: X", font=("Arial", 14))
        self.info_label.pack()

        self.timer_label = tk.Label(self.root, text="Время игры: 0 секунд", font=("Arial", 14))
        self.timer_label.pack()

        self.restart_button = tk.Button(
            self.root, text="Перезапустить игру", font=("Arial", 12), command=self.restart_game
        )
        self.restart_button.pack(pady=10)

    def set_mode(self, mode):
        self.game_mode = mode
        self.restart_game()

    def set_difficulty(self, level):
        self.difficulty = level
        self.restart_game()

    def make_move(self, index):
        if not self.game_started:
            self.start_time = time.time()
            self.game_started = True

        if self.board[index] or self.check_winner():
            return

        self.board[index] = self.current_player
        self.buttons[index].config(text=self.current_player)

        if self.check_winner():
            self.end_game(f"Победитель: {self.current_player}")
        elif "" not in self.board:
            self.end_game("Ничья!")
        else:
            self.switch_player()

            if self.current_player == "O" and self.game_mode == "AI":
                self.root.after(500, self.ai_move)

        self.update_timer()

    def ai_move(self):
        if self.difficulty == "Легкий ":
            self.ai_easy()
        elif self.difficulty == "Средний":
            self.ai_medium()
        elif self.difficulty == "Сложный":
            self.ai_hard()

    def ai_easy(self):
        empty_indices = [i for i, value in enumerate(self.board) if not value]
        if empty_indices:
            move = random.choice(empty_indices)
            self.make_move(move)

    def ai_medium(self):
        # Блокировка или выигрышный ход
        for symbol in ["O", "X"]:
            for i in range(9):
                board_copy = self.board[:]
                if not board_copy[i]:
                    board_copy[i] = symbol
                    if self.check_winner_in_board(board_copy, symbol):
                        self.make_move(i)
                        return
        self.ai_easy()

    def ai_hard(self):
        best_score = -float("inf")
        best_move = None

        for i in range(9):
            if not self.board[i]:
                self.board[i] = "O"
                score = self.minimax(self.board, 0, False)
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i

        if best_move is not None:
            self.make_move(best_move)

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner_in_board(board, "O"):
            return 1
        if self.check_winner_in_board(board, "X"):
            return -1
        if "" not in board:
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for i in range(9):
                if not board[i]:
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(9):
                if not board[i]:
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ""
                    best_score = min(score, best_score)
            return best_score

    def check_winner_in_board(self, board, symbol):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combination in winning_combinations:
            if all(board[i] == symbol for i in combination):
                return True
        return False

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"
        self.info_label.config(text=f"Текущий ход: {self.current_player}")

    def check_winner(self):
        return self.check_winner_in_board(self.board, self.current_player)

    def update_timer(self):
        if self.game_started:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Время игры: {elapsed_time} секунд")

    def end_game(self, message):
        self.game_started = False
        messagebox.showinfo("Игра окончена", message)

    def restart_game(self):
        self.board = [""] * 9
        self.current_player = "X"
        self.game_started = False
        self.start_time = None
        self.info_label.config(text="Текущий ход: X")
        self.timer_label.config(text="Время игры: 0 секунд")
        for button in self.buttons:
            button.config(text="")


# Запуск программы
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
