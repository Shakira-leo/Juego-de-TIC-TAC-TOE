import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.board = [" " for _ in range(9)]
        self.current_player = "X"  # El jugador siempre comienza como X
        self.is_ai = True  # Jugar contra IA
        self.difficulty = "Difícil"  # Dificultad predeterminada
        self.score_x = 0
        self.score_o = 0
        self.game_over = False  # Variable para controlar el fin del juego

        # Estilo de los botones
        self.buttons = []
        for i in range(9):
            button = tk.Button(master, text=" ", font='Arial 24', width=5, height=2,
                               bg="#ae7cea", activebackground="#71c9dd",
                               command=lambda i=i: self.player_move(i))
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            button.bind("<Enter>", lambda e: e.widget.config(bg="#ae7cea"))
            button.bind("<Leave>", lambda e: e.widget.config(bg="#ae7cea"))
            self.buttons.append(button)

        # Botón para reiniciar el juego
        self.reset_button = tk.Button(master, text="Reiniciar Juego", font='Arial 14', command=self.reset_game)
        self.reset_button.grid(row=3, columnspan=3, pady=10)

        # Etiqueta de dificultad
        self.difficulty_label = tk.Label(master, text=f"Dificultad: {self.difficulty}", font='Arial 14')
        self.difficulty_label.grid(row=4, column=0, columnspan=2)

        # Menú desplegable para seleccionar dificultad
        self.difficulty_menu = tk.StringVar(master)
        self.difficulty_menu.set(self.difficulty)
        self.difficulty_dropdown = tk.OptionMenu(master, self.difficulty_menu, "Fácil", "Intermedio", "Difícil", command=self.set_difficulty)
        self.difficulty_dropdown.grid(row=4, column=2)

        # Etiqueta de puntuación
        self.score_label = tk.Label(master, text=f"X: {self.score_x}  O: {self.score_o}", font='Arial 14')
        self.score_label.grid(row=5, columnspan=3)

    def player_move(self, index):
        """Handle player's move."""
        if self.board[index] == " " and not self.game_over:
            self.board[index] = "X"  # El jugador siempre juega como X
            self.buttons[index].config(text="X")
            if self.check_winner("X"):
                messagebox.showinfo("Ganador", "¡El jugador X ha ganado!")
                self.score_x += 1
                self.update_score()
                self.game_over = True  # Fin del juego
            elif " " not in self.board:
                messagebox.showinfo("Empate", "¡Es un empate!")
                self.game_over = True  # Fin del juego
            else:
                # Solo la IA juega después del movimiento del jugador
                if self.is_ai:
                    self.ai_move()

    def ai_move(self):
        """AI makes a move based on difficulty level."""
        if not self.game_over:
            index = self.minimax(self.board, "O")["index"]
            if index is not None:
                self.make_ai_move(index)

    def make_ai_move(self, index):
        """Make the AI's move on the board."""
        if index is not None and not self.game_over:
            self.board[index] = "O"
            self.buttons[index].config(text="O")
            if self.check_winner("O"):
                messagebox.showinfo("Ganador", "¡El jugador O ha ganado!")
                self.score_o += 1
                self.update_score()
                self.game_over = True  # Fin del juego

    def check_winner(self, player):
        """Check if the given player has won."""
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]
        
        return any(all(self.board[i] == player for i in combo) for combo in winning_combinations)

    def minimax(self, board, player):
        """Minimax algorithm to determine the best move for the AI."""
    
        if self.check_winner("O"):
            return {"score": 1}
    
        elif self.check_winner("X"):
            return {"score": -1}
    
        elif " " not in board:
            return {"score": 0}

        moves = []
    
        for i in range(9):
            if board[i] == " ":
                board[i] = player
                score = self.minimax(board, "X" if player == "O" else "O")["score"]
                board[i] = " "
                moves.append({"index": i, "score": score})

        best_move = max(moves, key=lambda x: x["score"]) if player == "O" else min(moves, key=lambda x: x["score"])

        return best_move

    def reset_game(self):
       """Reset the game board."""
       for i in range(len(self.buttons)):
           button = self.buttons[i]
           button.config(text=" ")
           button.config(bg="#87CEEB")

       # Reset game variables
       self.board = [" "] * 9
       self.current_player = "X"
       self.game_over = False

    def update_score(self):
       """Update the score display."""
       self.score_label.config(text=f"X: {self.score_x} O: {self.score_o}")

    def set_difficulty(self,difficulty):
       """Set the game difficulty."""
       self.difficulty = difficulty 
       self.difficulty_label.config(text=f"Dificultad: {self.difficulty}")

if __name__ == "__main__":
   root=tk.Tk()
   game=TicTacToe(root)
   root.mainloop()