
# Battleship Game

## Overview

The Battleship Game is a classic strategy game where players take turns guessing the locations of each other's ships on a grid. The game can be played with either two human players or one player against the computer. The objective is to sink all the opponent's ships before they sink yours.

## Features

- **Grid Size Selection**: Players can choose a grid size between 3x3 and 10x10 for varying levels of difficulty.
- **Player vs. Player or Player vs. Computer Modes**: The game supports two modes:
  - **Two Players**: Players alternate turns.
  - **Single Player**: The player competes against the computer.
- **Ship Placement**: Ships are randomly placed on the grid at the start of the game.
- **Guessing Mechanism**: Players input their guesses using a coordinate system (e.g., A1, B2).
- **Hit/Miss Feedback**: Players receive feedback on whether their guesses hit or missed a ship.
- **Turn-Based Gameplay**: Players take turns guessing locations until one player sinks all the opponent's ships.
- **Game End Conditions**: The game ends when one player sinks all of the opponent's ships or if there's a draw when both players hit the same number of ships.

## Installation

To run the Battleship game, ensure you have Python 3.x installed. Follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```
2. Navigate to the project directory:
   ```bash
   cd battleship_game
   ```
3. Run the game:
   ```bash
   python battleship.py
   ```

## Usage

1. Launch the game by executing the `battleship.py` file.
2. Select the grid size between 3 and 10 when prompted.
3. Choose the number of players (1 for computer mode, 2 for player vs. player).
4. Players will take turns to guess the locations of the ships using the format `<Letter><Number>` (e.g., A1).
5. The game displays the current state of the grid after each turn.
6. Continue playing until one player sinks all the opponent's ships or until a draw is declared.

## Code Explanation

The code is organized into a `BattleshipGame` class that encapsulates all game logic. Key components include:

- **Grid Creation**: A grid of specified size is initialized, filled with water (`~`).
- **Ship Placement**: Ships are randomly placed on the grid in empty locations (`S`).
- **User Input Handling**: The program prompts players for their guesses and validates the input.
- **Game Logic**: The program checks for hits or misses, updates the grid, and tracks the number of hits for each player.
- **Computer AI**: In single-player mode, the computer makes random guesses while ensuring it doesn't repeat previous guesses.

## Contribution

Contributions are welcome! If you'd like to enhance the game or report any bugs, please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the classic Battleship board game.
- Thank you to all contributors and testers who helped improve the game!
