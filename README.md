import tkinter as tk
import random


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-Нолики")
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.player_turn = True
        self.player_wins = 0
        self.computer_wins = 0
        self.draws = 0

        # Создание меню для выбора уровня сложности
        self.difficulty = tk.StringVar(value="Легкий")
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        difficulty_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Сложность", menu=difficulty_menu)
        difficulty_menu.add_radiobutton(label="Легкий", variable=self.difficulty, value="Легкий")
        difficulty_menu.add_radiobutton(label="Средний", variable=self.difficulty, value="Средний")
        difficulty_menu.add_radiobutton(label="Сложный", variable=self.difficulty, value="Сложный")

        # Показ счетчиков побед/поражений
        self.status_label = tk.Label(self.root, text="Игрок: 0 | Компьютер: 0 | Ничья: 0", font=('Arial', 15))
        self.status_label.grid(row=4, column=0, columnspan=3)

        self.create_board()

    def create_board(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.root, text=' ', font=('Arial', 40), width=5, height=2,
                                   command=lambda row=row, col=col: self.player_move(row, col))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def player_move(self, row, col):
        if self.board[row][col] == ' ' and self.player_turn:
            self.board[row][col] = 'X'
            self.buttons[row][col].config(text='X', state=tk.DISABLED)
            if self.check_winner('X'):
                self.highlight_winner('X')
                self.end_game("ПОЗДРАВЛЯЕМ! ВЫ ПОБЕДИЛИ!", "player")
            elif self.is_board_full():
                self.end_game("Ничья!", "draw")
            else:
                self.player_turn = False
                self.root.after(500, self.computer_move)

    def computer_move(self):
        if not self.player_turn:
            if self.difficulty.get() == "Легкий":
                self.random_move()
            elif self.difficulty.get() == "Средний":
                if not self.try_to_win('O'):
                    self.random_move()
            elif self.difficulty.get() == "Сложный":
                if not self.try_to_win('O'):
                    if not self.block_player('X'):
                        self.random_move()

            if self.check_winner('O'):
                self.end_game("Компьютер победил!", "computer")
            elif self.is_board_full():
                self.end_game("Ничья!", "draw")
            else:
                self.player_turn = True

    def random_move(self):
        while True:
            row = random.randint(0, 2)
            col = random.randint(0, 2)
            if self.board[row][col] == ' ':
                self.board[row][col] = 'O'
                self.buttons[row][col].config(text='O', state=tk.DISABLED)
                break

    def try_to_win(self, player):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    self.board[row][col] = player
                    if self.check_winner(player):
                        self.buttons[row][col].config(text='O', state=tk.DISABLED)
                        return True
                    self.board[row][col] = ' '
        return False

    def block_player(self, player):
        return self.try_to_win(player)

    def check_winner(self, player):
        # Проверка строк, столбцов и диагоналей
        for row in self.board:
            if all([cell == player for cell in row]):
                return True
        for col in range(3):
            if all([self.board[row][col] == player for row in range(3)]):
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return True
        return False

    def highlight_winner(self, player):
        # Подсветка победных крестиков красным цветом
        for row in range(3):
            if all([self.board[row][col] == player for col in range(3)]):
                for col in range(3):
                    self.buttons[row][col].config(fg='red')

        for col in range(3):
            if all([self.board[row][col] == player for row in range(3)]):
                for row in range(3):
                    self.buttons[row][col].config(fg='red')

        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            self.buttons[0][0].config(fg='red')
            self.buttons[1][1].config(fg='red')
            self.buttons[2][2].config(fg='red')

        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            self.buttons[0][2].config(fg='red')
            self.buttons[1][1].config(fg='red')
            self.buttons[2][0].config(fg='red')

    def is_board_full(self):
        return all([cell != ' ' for row in self.board for cell in row])

    def end_game(self, message, result):
        result_label = tk.Label(self.root, text=message, font=('Arial', 20))
        result_label.grid(row=3, column=0, columnspan=3)

        if result == "player":
            self.player_wins += 1
        elif result == "computer":
            self.computer_wins += 1
        elif result == "draw":
            self.draws += 1

        self.update_status()

        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(state=tk.DISABLED)

    def update_status(self):
        self.status_label.config(
            text=f"Игрок: {self.player_wins} | Компьютер: {self.computer_wins} | Ничья: {self.draws}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
