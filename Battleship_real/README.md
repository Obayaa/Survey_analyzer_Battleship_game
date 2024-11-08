# Battleship Game

This is a Battleship game implemented using Python and Tkinter. The game allows one player to compete against the computer, or two players to compete against each other on a customizable grid. Ships are placed on each player's grid, and the objective is to guess the positions of the opponent's ships.

## Features

- **Grid Customization**: Choose grid sizes between 10x10 and 15x15 for more flexibility.
- **Game Modes**: Supports both single-player (vs computer) and two-player modes.
- **Ship Placement**: Players can place ships manually, and the computer places ships randomly in single-player mode.
- **Turn-Based Gameplay**: Players take turns to make moves by selecting grid cells. The computer randomly selects cells during its turn.
- **Win Condition**: The game ends when all of one player's ships have been hit.

## How to Play

1. Start the game and select the grid size and game mode (1 Player or 2 Players).
2. Place ships on the grid by selecting cells. You can choose the orientation (horizontal or vertical) before placing each ship.
3. Once all ships are placed, take turns to guess the positions of the opponent’s ships by clicking cells on the opponent’s board.
4. The game ends when one player sinks all of the opponent's ships.

## Files and Components

- **BattleshipGame Class**: Manages the game logic, including ship placement, turns, and win conditions.
  - **place_ship**: Places ships on the board with validation to prevent overlap or out-of-bound placements.
  - **player_turn**: Manages the moves made by players, marking hits and misses.
  - **computer_turn**: Allows the computer to randomly select a cell for its turn in single-player mode.
  - **is_game_over**: Checks if all ships of one player are destroyed, indicating the end of the game.

- **BattleshipGUI Class**: Manages the GUI using Tkinter, allowing players to interact with the game.
  - **setup_gui**: Initializes the main interface, with options for game setup and status display.
  - **create_board_gui**: Creates interactive grid buttons for each player.
  - **start_game**: Initializes a new game instance and resets the game board.
  - **place_ship_gui**: Allows players to manually place ships on their boards in the chosen orientation.
  - **make_move**: Allows the current player to make a move on the opponent’s board.
  - **computer_move**: Handles the computer’s turn by choosing random cells.
  - **update_board_display**: Updates the grid colors to reflect hits, misses, and ship positions.
  - **show_game_over_message**: Displays the game-over message and asks if the player wants to play again.

## Installation and Running the Game

To run this game, make sure you have Python installed.

1. Download the code files.
2. Open a terminal in the code directory.
3. Run the following command:

    ```bash
    python battleship_game.py
    ```

## Requirements

- **Python 3.x** is required.
- **Tkinter** (included with most Python installations).

## GUI Layout

The GUI layout consists of:

- **Game Setup Panel**: Allows the selection of grid size and game mode.
- **Game Boards**: Player 1's and Player 2's grids are displayed side by side.
- **Status Bar**: Displays the current status of the game, like turn results and win messages.

## How Ships Work

Ships have different sizes:

- Carrier: 5 cells
- Battleship: 4 cells
- Cruiser: 3 cells
- Submarine: 3 cells
- Destroyer: 2 cells

Each ship must be placed horizontally or vertically within the grid limits. In single-player mode, the computer places ships randomly.

## Game Flow

1. Players place their ships.
2. Players take turns clicking on cells of the opponent’s board to guess ship positions.
3. Hits are marked with green, misses with red.
4. The first player to hit all of the opponent's ships wins the game.

---

Enjoy playing Battleship!
