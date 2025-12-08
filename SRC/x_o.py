import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")
        self.root.geometry("500x600")
        self.root.configure(bg="#f0f0f0")
        
        # Настройки игры
        self.board_size = 3
        self.current_player = "X"
        self.board = [["" for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.game_over = False
        self.score = {"X": 0, "O": 0, "Ничья": 0}
        self.against_computer = False
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление отображения счета
        self.update_score_display()
    
    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(
            self.root, 
            text="Крестики-нолики", 
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        title_label.pack(pady=10)
        
        # Панель счета
        self.score_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.score_frame.pack(pady=10)
        
        self.x_score_label = tk.Label(
            self.score_frame, 
            text="Крестики: 0", 
            font=("Arial", 14),
            bg="#ffcccc",
            fg="#333",
            width=12,
            relief="ridge"
        )
        self.x_score_label.pack(side=tk.LEFT, padx=5)
        
        self.o_score_label = tk.Label(
            self.score_frame, 
            text="Нолики: 0", 
            font=("Arial", 14),
            bg="#ccccff",
            fg="#333",
            width=12,
            relief="ridge"
        )
        self.o_score_label.pack(side=tk.LEFT, padx=5)
        
        self.draw_score_label = tk.Label(
            self.score_frame, 
            text="Ничьи: 0", 
            font=("Arial", 14),
            bg="#cccccc",
            fg="#333",
            width=12,
            relief="ridge"
        )
        self.draw_score_label.pack(side=tk.LEFT, padx=5)
        
        # Индикатор текущего игрока
        self.player_label = tk.Label(
            self.root, 
            text=f"Сейчас ходят: {self.current_player}", 
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        self.player_label.pack(pady=10)
        
        # Панель режима игры
        mode_frame = tk.Frame(self.root, bg="#f0f0f0")
        mode_frame.pack(pady=10)
        
        tk.Label(
            mode_frame, 
            text="Режим игры:", 
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#333"
        ).pack(side=tk.LEFT, padx=5)
        
        self.mode_var = tk.StringVar(value="player")
        
        tk.Radiobutton(
            mode_frame, 
            text="Два игрока", 
            variable=self.mode_var, 
            value="player",
            font=("Arial", 12),
            bg="#f0f0f0",
            command=self.change_mode
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Radiobutton(
            mode_frame, 
            text="Против компьютера", 
            variable=self.mode_var, 
            value="computer",
            font=("Arial", 12),
            bg="#f0f0f0",
            command=self.change_mode
        ).pack(side=tk.LEFT, padx=5)
        
        # Игровое поле
        self.buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.buttons_frame.pack(pady=20)
        
        self.buttons = []
        for i in range(self.board_size):
            row_buttons = []
            for j in range(self.board_size):
                button = tk.Button(
                    self.buttons_frame,
                    text="",
                    font=("Arial", 32, "bold"),
                    width=3,
                    height=1,
                    bg="#ffffff",
                    relief="ridge",
                    command=lambda row=i, col=j: self.make_move(row, col)
                )
                button.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(button)
            self.buttons.append(row_buttons)
        
        # Кнопка перезапуска
        restart_button = tk.Button(
            self.root,
            text="Новая игра",
            font=("Arial", 14),
            bg="#4CAF50",
            fg="white",
            width=15,
            height=1,
            command=self.reset_game
        )
        restart_button.pack(pady=10)
        
        # Кнопка сброса счета
        reset_score_button = tk.Button(
            self.root,
            text="Сбросить счет",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            width=15,
            height=1,
            command=self.reset_score
        )
        reset_score_button.pack(pady=5)
    
    def change_mode(self):
        """Изменение режима игры (игрок против игрока или игрок против компьютера)"""
        self.against_computer = (self.mode_var.get() == "computer")
        self.reset_game()
    
    def make_move(self, row, col):
        """Обработка хода игрока"""
        if self.game_over or self.board[row][col] != "":
            return
        
        # Ход игрока
        self.board[row][col] = self.current_player
        self.buttons[row][col].config(
            text=self.current_player,
            fg="#FF0000" if self.current_player == "X" else "#0000FF"
        )
        
        # Проверка на победу или ничью
        if self.check_winner():
            self.game_over = True
            messagebox.showinfo("Победа!", f"Игрок {self.current_player} победил!")
            self.score[self.current_player] += 1
            self.update_score_display()
            return
        elif self.check_draw():
            self.game_over = True
            messagebox.showinfo("Ничья!", "Игра завершилась вничью!")
            self.score["Ничья"] += 1
            self.update_score_display()
            return
        
        # Смена игрока
        self.current_player = "O" if self.current_player == "X" else "X"
        self.player_label.config(text=f"Сейчас ходят: {self.current_player}")
        
        # Если игра против компьютера и сейчас ход компьютера
        if self.against_computer and self.current_player == "O" and not self.game_over:
            self.root.after(500, self.computer_move)
    
    def computer_move(self):
        """Ход компьютера"""
        if self.game_over:
            return
        
        # Сначала проверяем, может ли компьютер выиграть
        move = self.find_winning_move("O")
        if not move:
            # Затем проверяем, может ли игрок выиграть следующим ходом
            move = self.find_winning_move("X")
            if not move:
                # Если нет, делаем случайный ход
                move = self.find_random_move()
        
        if move:
            row, col = move
            self.make_move(row, col)
    
    def find_winning_move(self, player):
        """Находит выигрышный ход для указанного игрока"""
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == "":
                    # Проверяем, будет ли это выигрышный ход
                    self.board[i][j] = player
                    if self.check_winner():
                        self.board[i][j] = ""
                        return (i, j)
                    self.board[i][j] = ""
        return None
    
    def find_random_move(self):
        """Находит случайный доступный ход"""
        available_moves = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == "":
                    available_moves.append((i, j))
        
        if available_moves:
            return random.choice(available_moves)
        return None
    
    def check_winner(self):
        """Проверка на победу"""
        # Проверка строк
        for i in range(self.board_size):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                # Подсветка выигрышной линии
                for j in range(self.board_size):
                    self.buttons[i][j].config(bg="#aaffaa")
                return True
        
        # Проверка столбцов
        for j in range(self.board_size):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] != "":
                # Подсветка выигрышной линии
                for i in range(self.board_size):
                    self.buttons[i][j].config(bg="#aaffaa")
                return True
        
        # Проверка диагоналей
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            # Подсветка выигрышной линии
            for i in range(self.board_size):
                self.buttons[i][i].config(bg="#aaffaa")
            return True
        
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            # Подсветка выигрышной линии
            for i in range(self.board_size):
                self.buttons[i][2 - i].config(bg="#aaffaa")
            return True
        
        return False
    
    def check_draw(self):
        """Проверка на ничью"""
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == "":
                    return False
        return True
    
    def reset_game(self):
        """Сброс игрового поля для новой игры"""
        self.current_player = "X"
        self.board = [["" for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.game_over = False
        
        # Сброс кнопок
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.buttons[i][j].config(text="", bg="#ffffff", fg="black")
        
        self.player_label.config(text=f"Сейчас ходят: {self.current_player}")
        
        # Если игра против компьютера и компьютер ходит первым
        if self.against_computer and self.current_player == "O":
            self.root.after(500, self.computer_move)
    
    def reset_score(self):
        """Сброс счета"""
        self.score = {"X": 0, "O": 0, "Ничья": 0}
        self.update_score_display()
    
    def update_score_display(self):
        """Обновление отображения счета"""
        self.x_score_label.config(text=f"Крестики: {self.score['X']}")
        self.o_score_label.config(text=f"Нолики: {self.score['O']}")
        self.draw_score_label.config(text=f"Ничьи: {self.score['Ничья']}")

def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()