
# Battleship Web Game

This project is a web-based implementation of the classic **Battleship** game. Developed with **Python Flask**, **HTML**, **CSS**, and **JavaScript**, this game allows players to compete against the computer in a grid-based naval battle, taking turns to guess the locations of each other's ships.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Gameplay](#gameplay)
- [File Structure](#file-structure)
- [Future Improvements](#future-improvements)
- [Screenshots](#Screenshots)

## Features

- **Single-player mode**: The player competes against an AI opponent.
- **Dynamic grid layout**: Grid size and ship placement adjust based on predefined configurations.
- **Turn-based gameplay**: Player and computer alternate turns, with updates shown in real-time.
- **Visual feedback**: Hit and miss statuses are displayed with colors and markers.
- **Game-over modal**: Declares the winner when all ships of a player are sunk.
- **Restart functionality**: Players can restart the game without refreshing the page.

## Technologies Used

- **Python (Flask)**: Backend logic, routing, and handling game state.
- **HTML**: Structure of the web interface.
- **CSS**: Styling and layout, including responsive design adjustments.
- **JavaScript**: Front-end logic, turn handling, and real-time updates.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Obayaa/Survey_analyzer_Battleship_game.git
   cd Survey_analyzer_Battleship_game
   ```

2. **Install Dependencies**:
   Make sure you have Python and Flask installed. You can set up a virtual environment and install dependencies as follows:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install flask
   ```

3. **Run the Game**:
   Start the Flask development server.
   ```bash
   flask run
   ```

4. **Open in Browser**:
   Go to `http://127.0.0.1:5000` in your web browser to start the game.

## Gameplay

1. **Objective**: The goal of the game is to sink all of the opponent's ships before they sink yours.
2. **Turn-Based System**:
   - **Player's Turn**: Click on a cell in the computer's grid to make a guess.
   - **Computer's Turn**: After the player’s move, the computer makes a move on the player’s grid.
3. **End of Game**: When all ships of either the player or the computer are sunk, a message will appear declaring the winner.

## File Structure

- **app.py**: Main Flask application file to initialize and run the server.
- **battleship_logic.py**: This file handles all the logic for the game.
- **requirement.txt**: This file contains all the dependancies used in the game.
- **templates/**: Contains the HTML files, including the main game page.
  - `index.html`: The main interface for the game.
  - `game.html`: The main interface for the game.
  - `help.html`: The interface that explains the rules of the game.
- **images/**: Holds all the screenshots of the game.
- **static/**: Holds all static files.
  - **css/**: Contains `styles.css` for custom styling.
  - **js/**: Contains `game.js` for JavaScript game logic.


## Future Improvements

- **Multiplayer Mode**: Allow two players to play against each other.
- **Difficulty Levels**: Add AI difficulty levels to make the game more challenging.
- **Animated Transitions**: Enhance the visual experience with smooth transitions between turns.
- **Score Tracking**: Implement a scoreboard to keep track of wins and losses across sessions.
- **Mobile Responsiveness**: Improve design for mobile-friendly gameplay.

## Screenshots

![Screenshot of Battleship Game](https://github.com/Obayaa/Survey_analyzer_Battleship_game/blob/main/battleship_game_web/images/main_screen.png)
![Screenshot of Battleship Game Popup](https://github.com/Obayaa/Survey_analyzer_Battleship_game/blob/main/battleship_game_web/img/pop_up.png)
![Screenshot of Battleship Game Help Page](https://github.com/Obayaa/Survey_analyzer_Battleship_game/blob/main/battleship_game_web/img/help_page.png)
