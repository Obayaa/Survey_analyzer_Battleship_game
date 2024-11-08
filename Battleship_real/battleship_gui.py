import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple
import random

class BattleshipGame:
    # Ship sizes and names
    SHIPS = [(5, "Carrier"), (4, "Battleship"), (3, "Cruiser"), (3, "Submarine"), (2, "Destroyer")]

    def __init__(self, grid_size: int, is_two_player: bool):
        self.grid_size = grid_size
        self.is_two_player = is_two_player
        self.player1_board = [["~"] * grid_size for _ in range(grid_size)]
        self.player2_board = [["~"] * grid_size for _ in range(grid_size)]
        self.player1_ships = []
        self.player2_ships = []
        self.current_turn = 1
        self.game_over = False

    def place_computer_ships(self):
        for size, name in self.SHIPS:
            placed = False
            while not placed:
                row = random.randint(0, self.grid_size - 1)
                col = random.randint(0, self.grid_size - 1)
                orientation = random.choice(["horizontal", "vertical"])
                placed = self.place_ship(2, row, col, size, orientation)
                if placed:
                    self.player2_ships.append((row, col, size, orientation, name))

    def place_ship(self, player: int, row: int, col: int, size: int, orientation: str) -> bool:
        board = self.player1_board if player == 1 else self.player2_board
        
        # Check if the ship is within bounds and doesn't overlap
        if orientation == "horizontal":
            if col + size > self.grid_size:
                return False  # Ship goes out of bounds horizontally
            for i in range(size):
                if board[row][col + i] != "~":  # Check for overlap
                    return False
            # Place ship horizontally
            for i in range(size):
                board[row][col + i] = "S"
        elif orientation == "vertical":
            if row + size > self.grid_size:
                return False  # Ship goes out of bounds vertically
            for i in range(size):
                if board[row + i][col] != "~":  # Check for overlap
                    return False
            # Place ship vertically
            for i in range(size):
                board[row + i][col] = "S"
        
        return True

    def player_turn(self, player: int, row: int, col: int) -> str:
        board = self.player2_board if player == 1 else self.player1_board
        # Simple attack logic
        if board[row][col] == "~":
            board[row][col] = "M"  # Miss
            return "Miss!"
        elif board[row][col] == "S":
            board[row][col] = "X"  # Hit
            
            # Check if ship has been sunk
            for ship in (self.player2_ships if player == 1 else self.player1_ships):
                ship_row, ship_col, ship_size, ship_orientation, ship_name = ship
                if ship_orientation == "horizontal":
                    if all(board[ship_row][ship_col + i] == "X" for i in range(ship_size)):
                        print(f"{ship_name} sunk!")
                else:
                    if all(board[ship_row + i][ship_col] == "X" for i in range(ship_size)):
                        print(f"{ship_name} sunk!")
            return "Hit!"
        else:
            return "Already attacked!"

    def computer_turn(self) -> Tuple[int, int, str]:
        # Randomly select a move for the computer
        row, col = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
        result = self.player_turn(2, row, col)
        return row, col, result

    def is_game_over(self) -> Tuple[bool, str]:
        # Check if all ships for Player 2 (Computer or Player 2) are hit
        if all(cell != "S" for row in self.player2_board for cell in row):
            return True, "Player 1 wins!"
        
        # Check if all ships for Player 1 are hit
        if all(cell != "S" for row in self.player1_board for cell in row):
            return True, "Player 2 wins!" if self.is_two_player else "Computer wins!"

        return False, ""

class BattleshipGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Battleship Game")
        self.game = None
        self.buttons = []
        self.setup_gui()

    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Game setup frame
        setup_frame = ttk.LabelFrame(main_frame, text="Game Setup", padding="5")
        setup_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))

        # Grid size selection
        ttk.Label(setup_frame, text="Grid Size:").grid(row=0, column=0, padx=5)
        self.grid_size_var = tk.StringVar(value="10")
        grid_size_combo = ttk.Combobox(setup_frame, textvariable=self.grid_size_var, 
                                     values=list(range(10, 16)), width=5, state="readonly")
        grid_size_combo.grid(row=0, column=1, padx=5)

        # Game mode selection
        ttk.Label(setup_frame, text="Game Mode:").grid(row=0, column=2, padx=5)
        self.game_mode_var = tk.StringVar(value="1")
        mode_frame = ttk.Frame(setup_frame)
        mode_frame.grid(row=0, column=3, padx=5)
        ttk.Radiobutton(mode_frame, text="1 Player", variable=self.game_mode_var, 
                       value="1").grid(row=0, column=0)
        # ttk.Radiobutton(mode_frame, text="2 Players", variable=self.game_mode_var, 
        #                value="2").grid(row=0, column=1)

        # Start button
        ttk.Button(setup_frame, text="Start New Game", 
                  command=self.start_game).grid(row=0, column=4, padx=10)

        # Game boards frame
        self.boards_frame = ttk.Frame(main_frame)
        self.boards_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # Status bar
        self.status_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=2, column=0, 
                                                                columnspan=2, pady=5)

    def create_board_gui(self, frame, board, is_opponent=False):
        buttons = []
        for i in range(self.game.grid_size):
            row_buttons = []
            for j in range(self.game.grid_size):
                btn = tk.Button(frame, width=3, bg="light blue")  # Default ocean color
                btn.grid(row=i + 1, column=j + 1, padx=1, pady=1)
                if is_opponent:
                    btn.configure(command=lambda r=i, c=j: self.make_move(r, c))
                else:
                    btn.configure(command=lambda r=i, c=j: self.place_ship_gui(r, c))  # Bind to place ship
                row_buttons.append(btn)
            buttons.append(row_buttons)
        return buttons

    def start_game(self):
        grid_size = int(self.grid_size_var.get())
        is_two_player = self.game_mode_var.get() == "2"
        self.game = BattleshipGame(grid_size, is_two_player)
        
        # Clear existing boards
        for widget in self.boards_frame.winfo_children():
            widget.destroy()

        # Create player boards
        player1_frame = ttk.LabelFrame(self.boards_frame, text="Player 1's Board")
        player1_frame.grid(row=0, column=0, padx=10)
        
        opponent_frame = ttk.LabelFrame(self.boards_frame, 
                                      text="Player 2's Board" if is_two_player else "Computer's Board")
        opponent_frame.grid(row=0, column=1, padx=10)

        # Create buttons for boards
        self.player1_buttons = self.create_board_gui(player1_frame, self.game.player1_board)
        self.opponent_buttons = self.create_board_gui(opponent_frame, self.game.player2_board, True)

        self.status_var.set("Place your ships!")
        self.place_ships()
        
        # Place computer ships if it's a single-player game
        if not is_two_player:
            self.game.place_computer_ships()
            print("Computer ships placed:", self.game.player2_ships)  # For debugging

    def place_ship_gui(self, row, col):
        if self.current_ship_index < len(BattleshipGame.SHIPS):
            size, name = BattleshipGame.SHIPS[self.current_ship_index]
            orientation = self.orientation_var.get()
            if self.game.place_ship(1, row, col, size, orientation):
                # Color the cells to represent the ship
                for i in range(size):
                    if orientation == "horizontal":
                        self.player1_buttons[row][col + i].configure(bg="gray")  # Color ship segment
                    else:
                        self.player1_buttons[row + i][col].configure(bg="gray")
                self.current_ship_index += 1
                self.update_ship_label()
            else:
                messagebox.showerror("Invalid Placement", "This placement is not allowed.")
        if self.current_ship_index == len(BattleshipGame.SHIPS):
            self.status_var.set("All ships placed! Start the game.")

    def place_ships(self):
        # Ship placement dialog implementation
        ship_window = tk.Toplevel(self.root)
        ship_window.title("Place Ships")
        ship_window.transient(self.root)
        
        ttk.Label(ship_window, 
                 text="Click on the board and choose orientation to place ships").pack(pady=5)
        
        self.current_ship_index = 0
        self.current_ship_var = tk.StringVar()
        self.update_ship_label()
        
        ttk.Label(ship_window, textvariable=self.current_ship_var).pack(pady=5)
        
        orientation_frame = ttk.Frame(ship_window)
        orientation_frame.pack(pady=5)
        
        self.orientation_var = tk.StringVar(value="horizontal")
        ttk.Radiobutton(orientation_frame, text="Horizontal", 
                       variable=self.orientation_var, value="horizontal").pack(side=tk.LEFT)
        ttk.Radiobutton(orientation_frame, text="Vertical", 
                       variable=self.orientation_var, value="vertical").pack(side=tk.LEFT)

    def update_ship_label(self):
        if self.current_ship_index < len(BattleshipGame.SHIPS):
            size, name = BattleshipGame.SHIPS[self.current_ship_index]
            self.current_ship_var.set(f"Placing {name} (size: {size})")
        else:
            self.current_ship_var.set("All ships placed!")

    def make_move(self, row: int, col: int):
        if not self.game or self.game.is_game_over()[0]:
            return

        result = self.game.player_turn(1, row, col)
        self.update_board_display()
        self.status_var.set(result)

        # Check if Player 1 won
        game_over, message = self.game.is_game_over()
        if game_over:
            self.show_game_over_message(message)
            return

        if not self.game.is_two_player:
            self.root.after(1000, self.computer_move)

    def computer_move(self):
        """Handle computer's random attack on player board."""
        row, col, result = self.game.computer_turn()
        self.update_board_display()
        self.status_var.set(f"Computer: {result}")

        game_over, message = self.game.is_game_over()
        if game_over:
            self.show_game_over_message(message)


    def update_board_display(self):
        """Update the player and opponent board display with colors for hits and misses."""
        # Update Player 1's board
        for i in range(self.game.grid_size):
            for j in range(self.game.grid_size):
                cell = self.game.player1_board[i][j]
                button = self.player1_buttons[i][j]
                if cell == "M":  # Miss
                    button.configure(bg="red")  # Color for miss
                elif cell == "X":  # Hit
                    button.configure(bg="green")  # Color for hit
                elif cell == "S":  # Ship, keep it gray if revealed
                    button.configure(bg="gray")

        # Update Opponent's board (Player 2 or Computer)
        for i in range(self.game.grid_size):
            for j in range(self.game.grid_size):
                cell = self.game.player2_board[i][j]
                button = self.opponent_buttons[i][j]
                if cell == "M":  # Miss
                    button.configure(bg="red")  # Color for miss
                elif cell == "X":  # Hit
                    button.configure(bg="green")  # Color for hit
                # Do not reveal ships for opponent; only show hits/misses

    def show_game_over_message(self, message):
        messagebox.showinfo("Game Over", message)
        if messagebox.askyesno("Play Again?", "Would you like to play again?"):
            self.start_game()
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BattleshipGUI(root)
    root.mainloop()