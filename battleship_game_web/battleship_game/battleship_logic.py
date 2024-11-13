import random

class BattleshipGame:
    def __init__(self):
        self.grid_size = 10
        self.player_board = []
        self.computer_board = []
        self.player_ships = []
        self.computer_ships = []
        self.game_over = False
        self.winner = None
        
        # Define the ship types and their sizes
        self.ship_types = {
            5: "Carrier",
            4: "Battleship",
            3: "Cruiser",
            3: "Submarine",
            2: "Destroyer"
        }
        
        # Tracks the ships and their hits
        self.player_ship_hits = {}
        self.computer_ship_hits = {}

    def __getstate__(self):
        # Return state as a dict
        return self.__dict__

    def __setstate__(self, state):
        # Restore instance attributes
        self.__dict__.update(state)

    def new_game(self, size):
        self.grid_size = size
        self.player_board = [['' for _ in range(size)] for _ in range(size)]
        self.computer_board = [['' for _ in range(size)] for _ in range(size)]
        self.game_over = False
        self.winner = None
        self.player_ship_hits = {}
        self.computer_ship_hits = {}
        self.player_ships = self.place_ships(self.player_board)
        self.computer_ships = self.place_ships(self.computer_board)  
        
    def place_ships(self, board):
        ship_sizes = [5, 4, 3, 3, 2]
        ships = []
        ship_count = 1
        for size in ship_sizes:
            placed = False
            while not placed:
                orientation = random.choice(['H', 'V'])
                row = random.randint(0, self.grid_size - 1)
                col = random.randint(0, self.grid_size - 1)
                if self.can_place_ship(board, row, col, size, orientation):
                    ship_positions = self.mark_ship(board, row, col, size, orientation)
                    ship_id = f"{self.ship_types.get(size, 'Ship')}_{ship_count}"
                    ships.append({"id": ship_id, "positions": ship_positions, "size": size})
                    if board == self.player_board:
                        self.player_ship_hits[ship_id] = 0
                    else:
                        self.computer_ship_hits[ship_id] = 0
                    placed = True
            ship_count += 1
        return ships

    def can_place_ship(self, board, row, col, size, orientation):
        if orientation == 'H' and col + size > self.grid_size:
            return False
        if orientation == 'V' and row + size > self.grid_size:
            return False
        for i in range(size):
            if orientation == 'H' and board[row][col + i] == 'S':
                return False
            if orientation == 'V' and board[row + i][col] == 'S':
                return False
        return True

    def mark_ship(self, board, row, col, size, orientation):
        positions = []
        for i in range(size):
            if orientation == 'H':
                board[row][col + i] = 'S'
                positions.append((row, col + i))
            else:
                board[row + i][col] = 'S'
                positions.append((row + i, col))
        return positions

    def make_move(self, row, col, is_player=True):
        if self.game_over:
            return {"result": "game_over", "winner": self.winner}

        board = self.computer_board if is_player else self.player_board
        ships = self.computer_ships if is_player else self.player_ships
        ship_hits = self.computer_ship_hits if is_player else self.player_ship_hits
        target = "computer" if is_player else "player"
        message = ""

        # Check if cell was already hit
        if board[row][col] in ['H', 'M']:
            return {"result": "invalid", "message": "This cell was already targeted"}

        if board[row][col] == 'S':
            board[row][col] = 'H'
            # Find which ship was hit
            hit_ship = None
            for ship in ships:
                if (row, col) in ship["positions"]:
                    hit_ship = ship
                    ship_hits[ship["id"]] += 1
                    break
            
            # Check if ship was sunk
            if hit_ship and ship_hits[hit_ship["id"]] == hit_ship["size"]:
                message = f"{hit_ship['id']} was sunk!"
            else:
                message = "Hit!"
            
            result = {"result": "hit", "row": row, "col": col, "target": target, "message": message}
        else:
            board[row][col] = 'M'
            message = "Miss!"
            result = {"result": "miss", "row": row, "col": col, "target": target, "message": message}

        # Check for game over
        if self.all_ships_sunk(self.computer_board if is_player else self.player_board):
            self.game_over = True
            self.winner = "Player" if is_player else "Computer"
            result["game_over"] = True
            result["winner"] = self.winner

        return result


    def computer_turn(self):
        row, col = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
        while self.player_board[row][col] in ['H', 'M']:
            row, col = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
        
        # Computer makes a move
        result = self.make_move(row, col, is_player=False)
        
        # Check for game over condition again after computer's move
        if self.all_ships_sunk(self.player_board):
            result["game_over"] = True
            result["winner"] = "Computer"
        
        return result

        
    def all_ships_sunk(self, board):
        return not any('S' in row for row in board)
