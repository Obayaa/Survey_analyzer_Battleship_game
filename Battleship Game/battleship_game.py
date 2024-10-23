import random
import string
import time  # Import time module to add delay


class BattleshipGame:
    def __init__(self, size, num_players):
        self.size = size
        self.grid = self.create_grid(size)
        self.num_ships = size  # Total number of ships on the grid
        self.ships_left = self.num_ships  # Shared number of ships left for both players
        self.num_players = num_players
        self.player_hits = [0, 0]  # Track hits for Player 1 and Player 2
        self.place_ships()  # Place ships on the shared grid

    def create_grid(self, size):
        """Creates a grid initialized with '~'."""
        return [['~' for _ in range(size)] for _ in range(size)]

    def print_grid(self, show_ships=False):
        """Prints the grid showing only hits and misses unless show_ships is True."""
        print("  " + " ".join(string.ascii_uppercase[:self.size]))
        for i, row in enumerate(self.grid):
            if show_ships:
                print(f"{i + 1} " + " ".join(row))
            else:
                print(f"{i + 1} " + " ".join('H' if cell == 'H' else 'M' if cell == 'M' else '~' for cell in row))

    def place_ships(self):
        """Randomly places ships on the grid."""
        ships_placed = 0
        while ships_placed < self.num_ships:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if self.grid[row][col] == '~':
                self.grid[row][col] = 'S'
                ships_placed += 1

    def get_user_guess(self, player):
        """Prompts the user for a guess and validates it."""
        while True:
            guess = input(f"{player}, enter your guess (e.g., A1): ").upper()
            if len(guess) < 2 or not guess[0].isalpha() or not guess[1:].isdigit():
                print("Invalid input! Please use format like A1.")
                continue

            col = string.ascii_uppercase.index(guess[0])
            row = int(guess[1:]) - 1

            if 0 <= row < self.size and 0 <= col < self.size:
                if self.grid[row][col] == 'H' or self.grid[row][col] == 'M':
                    print(f"{player}, you already guessed that spot! Try again.")
                else:
                    return row, col
            else:
                print("Guess is off-grid! Try again.")

    def check_guess(self, row, col, player):
        """Mark hit or miss on the grid and return True if it's a hit."""
        if self.grid[row][col] == 'S':
            print(f"{player} hits a ship!")
            self.grid[row][col] = 'H'
            self.ships_left -= 1
            if player == "Player 1":
                self.player_hits[0] += 1  # Increment Player 1 hits
            else:
                self.player_hits[1] += 1  # Increment Player 2 hits
            return True
        else:
            print(f"{player} misses.")
            self.grid[row][col] = 'M'
            return False

    def computer_turn(self):
        """Handles the computer's turn."""
        print("\nComputer is thinking...")
        time.sleep(2)  # Add delay to simulate thinking
        while True:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if self.grid[row][col] == '~' or self.grid[row][col] == 'S':
                print(f"Computer guessed: {string.ascii_uppercase[col]}{row + 1}")
                if self.grid[row][col] == 'S':
                    print("The computer hit a ship!")
                    self.grid[row][col] = 'H'
                    self.ships_left -= 1
                    self.player_hits[1] += 1  # Increment computer hits
                else:
                    print("The computer missed!")
                    self.grid[row][col] = 'M'
                break

    def check_win(self):
        """Checks if there are any ships left."""
        return self.ships_left == 0

    def check_draw(self):
        """Checks for a draw condition."""
        if self.player_hits[0] == self.player_hits[1] and self.ships_left == 0:
            return True
        return False

    def play(self):
        """Main game loop."""
        print(f"Starting Battleship! Grid size: {self.size}x{self.size}")
        current_player = 1

        while True:
            print("\nGame board:")
            self.print_grid()

            # Player turn logic
            if current_player == 1:
                row, col = self.get_user_guess("Player 1")
                self.check_guess(row, col, "Player 1")
                if self.check_win():
                    print("Congratulations, Player 1! You sunk the most ships! You won!")
                    break
                current_player = 2  # Switch turn to Player 2 or Computer
            else:
                if self.num_players == 2:
                    row, col = self.get_user_guess("Player 2")
                    self.check_guess(row, col, "Player 2")
                    if self.check_win():
                        print("Congratulations, Player 2! You sunk the most ships! You won!")
                        break
                    current_player = 1  # Switch turn back to Player 1
                else:
                    self.computer_turn()
                    if self.check_win():
                        print("All ships are sunk! The computer won.")
                        break
                    current_player = 1  # Switch turn back to Player 1

            # Check for draw condition
            if self.check_draw():
                print("It's a draw! Both players hit the same number of ships.")
                break

            # Display remaining ships
            print(f"\nShips left: {self.ships_left}")

# Game setup with grid size validation
def get_grid_size():
    while True:
        try:
            size = int(input("Enter the grid size (3-10): "))
            if 3 <= size <= 10:
                return size
            else:
                print("Invalid input! Please enter a number between 3 and 10.")
        except ValueError:
            print("Please enter a valid integer.")

# Game setup with number of players validation
def get_num_players():
    while True:
        try:
            num_players = int(input("Enter number of players (1 or 2): "))
            if num_players in [1, 2]:
                return num_players
            else:
                print("Invalid input! Please enter 1 or 2.")
        except ValueError:
            print("Please enter a valid integer.")

# Get grid size and player count
size = get_grid_size()
num_players = get_num_players()

# Start the game
game = BattleshipGame(size, num_players)
game.play()