import random
from enum import Enum
from typing import List, Tuple, Set

class GameAborted(Exception):
    """Exception raised when game is aborted."""
    pass

class CellState(Enum):
    EMPTY = "."
    SHIP = "S"
    HIT = "X"
    MISS = "O"

class Ship:
    def __init__(self, size: int, name: str):
        self.size = size
        self.name = name
        self.coordinates: Set[Tuple[int, int]] = set()
        self.hits: Set[Tuple[int, int]] = set()

    @property
    def is_sunk(self) -> bool:
        return len(self.hits) == self.size

class Board:
    def __init__(self, size: int = 10):
        self.size = size
        self.grid = [[CellState.EMPTY for _ in range(size)] for _ in range(size)]
        self.ships: List[Ship] = []
        
    def place_ship(self, ship: Ship, start_row: int, start_col: int, is_horizontal: bool) -> bool:
        coordinates = self._get_ship_coordinates(ship.size, start_row, start_col, is_horizontal)
        if not coordinates:
            return False
            
        for row, col in coordinates:
            self.grid[row][col] = CellState.SHIP
        ship.coordinates = set(coordinates)
        self.ships.append(ship)
        return True
    
    def _get_ship_coordinates(self, size: int, start_row: int, start_col: int, is_horizontal: bool) -> List[Tuple[int, int]]:
        coordinates = []
        for i in range(size):
            row = start_row if is_horizontal else start_row + i
            col = start_col + i if is_horizontal else start_col
            
            if not (0 <= row < self.size and 0 <= col < self.size):
                return []
            if self.grid[row][col] != CellState.EMPTY:
                return []
                
            coordinates.append((row, col))
        return coordinates

    def receive_attack(self, row: int, col: int) -> Tuple[bool, Ship | None]:
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False, None
            
        cell = self.grid[row][col]
        if cell == CellState.HIT or cell == CellState.MISS:
            return False, None
            
        is_hit = cell == CellState.SHIP
        self.grid[row][col] = CellState.HIT if is_hit else CellState.MISS
        
        if is_hit:
            for ship in self.ships:
                if (row, col) in ship.coordinates:
                    ship.hits.add((row, col))
                    return True, ship
        return True, None

    def display(self, hide_ships: bool = False) -> str:
        header = "   " + " ".join(f"{i:2d}" for i in range(self.size))
        rows = [header]
        
        for i, row in enumerate(self.grid):
            cells = []
            for cell in row:
                if hide_ships and cell == CellState.SHIP:
                    cells.append(CellState.EMPTY.value)
                else:
                    cells.append(cell.value)
            rows.append(f"{i:2d} {' '.join(cells)}")
        return "\n".join(rows)

class BattleshipGame:
    SHIPS = [
        (5, "Carrier"),
        (4, "Battleship"),
        (3, "Cruiser"),
        (3, "Submarine"),
        (2, "Destroyer")
    ]
    
    def __init__(self, grid_size: int, is_two_player: bool):
        self.grid_size = grid_size
        self.is_two_player = is_two_player
        self.player1_board = Board(grid_size)
        self.player2_board = Board(grid_size)
        self.is_aborted = False
        
    def abort_game(self):
        """Abort the current game."""
        self.is_aborted = True
        raise GameAborted("Game aborted by player!")

    def place_computer_ships(self):
        """Place ships randomly for computer player"""
        for size, name in self.SHIPS:
            while True:
                row = random.randint(0, self.grid_size - 1)
                col = random.randint(0, self.grid_size - 1)
                is_horizontal = random.choice([True, False])
                if self.player2_board.place_ship(Ship(size, name), row, col, is_horizontal):
                    break

    def player_turn(self, player_num: int, row: int, col: int) -> str:
        target_board = self.player2_board if player_num == 1 else self.player1_board
        valid, ship = target_board.receive_attack(row, col)
        
        if not valid:
            return "Invalid attack position!"
        
        if ship:
            if ship.is_sunk:
                return f"Hit! You sunk the {ship.name}!"
            return "Hit!"
        return "Miss!"

    def computer_turn(self) -> Tuple[int, int, str]:
        while True:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            valid, ship = self.player1_board.receive_attack(row, col)
            if valid:
                break
        
        result = "Miss!"
        if ship:
            result = f"Hit! Your {ship.name} was hit!"
            if ship.is_sunk:
                result = f"Hit! Your {ship.name} was sunk!"
        
        return row, col, result

    def is_game_over(self) -> Tuple[bool, str]:
        if self.is_aborted:
            return True, "Game aborted!"
            
        player1_won = all(ship.is_sunk for ship in self.player2_board.ships)
        player2_won = all(ship.is_sunk for ship in self.player1_board.ships)
        
        if player1_won:
            return True, "Congratulations! Player 1 won!"
        if player2_won:
            winner = "Player 2" if self.is_two_player else "Computer"
            return True, f"Game Over! {winner} won!"
        return False, ""

    def display_boards(self, current_player: int):
        if current_player == 1:
            print("\nPlayer 1's Board:")
            print(self.player1_board.display())
            print("\nOpponent's Board:")
            print(self.player2_board.display(hide_ships=True))
        else:
            print("\nPlayer 2's Board:")
            print(self.player2_board.display())
            print("\nOpponent's Board:")
            print(self.player1_board.display(hide_ships=True))

def play_game():
    print("Welcome to Battleship!")
    
    # Game setup
    while True:
        try:
            grid_size = int(input("Enter grid size (10-15): "))
            if 10 <= grid_size <= 15:
                break
            print("Grid size must be between 10 and 15!")
        except ValueError:
            print("Please enter a valid number!")
    
    while True:
        mode = input("Select game mode (1 for Single Player, 2 for Two Players): ")
        if mode in ['1', '2']:
            break
        print("Please enter 1 or 2!")
    
    is_two_player = mode == '2'
    game = BattleshipGame(grid_size, is_two_player)
    print("\nPlace your ships:")
    print("(Press Ctrl+C at any time to abort the game)")
    
    try:
        # Player 1 ship placement
        print("\nPlayer 1, place your ships:")
        for size, name in BattleshipGame.SHIPS:
            game.display_boards(1)
            while True:
                try:
                    print(f"\nPlacing {name} (size: {size})")
                    row = int(input(f"Enter row (0-{grid_size-1}): "))
                    col = int(input(f"Enter column (0-{grid_size-1}): "))
                    is_horizontal = input("Place horizontally? (y/n): ").lower() == 'y'
                    
                    if game.player1_board.place_ship(Ship(size, name), row, col, is_horizontal):
                        break
                    print("Invalid placement! Try again.")
                except ValueError:
                    print("Invalid input! Please enter valid numbers.")
        
        # Player 2 / Computer ship placement
        if is_two_player:
            print("\nPlayer 2, place your ships:")
            for size, name in BattleshipGame.SHIPS:
                game.display_boards(2)
                while True:
                    try:
                        print(f"\nPlacing {name} (size: {size})")
                        row = int(input(f"Enter row (0-{grid_size-1}): "))
                        col = int(input(f"Enter column (0-{grid_size-1}): "))
                        is_horizontal = input("Place horizontally? (y/n): ").lower() == 'y'
                        
                        if game.player2_board.place_ship(Ship(size, name), row, col, is_horizontal):
                            break
                        print("Invalid placement! Try again.")
                    except ValueError:
                        print("Invalid input! Please enter valid numbers.")
        else:
            print("\nComputer is placing ships...")
            game.place_computer_ships()
        
        # Main game loop
        current_player = 1
        while True:
            game.display_boards(current_player)
            
            if current_player == 1:
                # Player 1's turn
                while True:
                    try:
                        print("\nPlayer 1's turn!")
                        row = int(input(f"Enter attack row (0-{grid_size-1}): "))
                        col = int(input(f"Enter column (0-{grid_size-1}): "))
                        result = game.player_turn(1, row, col)
                        print(result)
                        break
                    except ValueError:
                        print("Invalid input! Please enter valid numbers.")
            else:
                if is_two_player:
                    # Player 2's turn
                    while True:
                        try:
                            print("\nPlayer 2's turn!")
                            row = int(input(f"Enter attack row (0-{grid_size-1}): "))
                            col = int(input(f"Enter column (0-{grid_size-1}): "))
                            result = game.player_turn(2, row, col)
                            print(result)
                            break
                        except ValueError:
                            print("Invalid input! Please enter valid numbers.")
                else:
                    # Computer's turn
                    input("\nPress Enter for computer's turn (or Ctrl+C to abort)...")
                    row, col, result = game.computer_turn()
                    print(f"\nComputer attacked position ({row}, {col})")
                    print(result)
            
            # Check for game over
            game_over, message = game.is_game_over()
            if game_over:
                game.display_boards(current_player)
                print(message)
                break
            
            # Switch players
            current_player = 3 - current_player  # Switches between 1 and 2
                
    except KeyboardInterrupt:
        print("\nGame aborted by player!")
    except GameAborted:
        print("\nGame aborted!")

if __name__ == "__main__":
    play_game()