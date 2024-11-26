from flask import Flask, render_template, request, jsonify, session
from battleship_logic import BattleshipGame
import pickle

app = Flask(__name__)
app.secret_key = 'battleship_dev_key_2024'  # Required for session management

@app.route('/')
def index():
    """
    Renders the main page of the game.
    """
    return render_template('index.html')

@app.route('/help')
def help_page():
    return render_template('help.html')


@app.route('/start_game', methods=['POST', 'GET'])
def start_game():
    """
    Starts a new game by creating an instance of the BattleshipGame class.
    Retrieves the grid size from the form and stores the game state in the session.
    """
    try:
        # Get grid size and validate it
        grid_size = int(request.form.get('grid_size', 10))
        if grid_size < 10 or grid_size > 15:
            raise ValueError("Grid size must be between 10 and 15.")
        
        # Start a new game with the selected grid size
        game = BattleshipGame()
        game.new_game(grid_size)
        
        # Store the game state in the session using pickle
        session['game'] = pickle.dumps(game)
        
        return render_template('game.html', grid_size=grid_size, player_board=game.player_board)
    
    except Exception as e:
        # Return an error message if something goes wrong
        return jsonify({"error": str(e)}), 400

@app.route('/make_move', methods=['POST'])
def make_move():
    """
    Handles the player's move by receiving the row and column from the frontend,
    and updates the game state.
    """
    # Retrieve game state from session
    game = pickle.loads(session['game'])
    
    # Get the row and column for the player's move from the request
    row = int(request.json['row'])
    col = int(request.json['col'])
    
    # Player's move
    player_result = game.make_move(row, col)
    
    # Save game state
    session['game'] = pickle.dumps(game)
    
    # Return the result of the player's move
    return jsonify({"player": player_result})

@app.route('/computer_turn', methods=['POST'])
def computer_turn():
    """
    Handles the computer's turn by making a move and updating the game state.
    """
    # Retrieve game state from session
    game = pickle.loads(session['game'])
    
    # Computer's move
    computer_result = game.computer_turn()
    
    # Save updated game state
    session['game'] = pickle.dumps(game)
    
    # Return the result of the computer's move
    return jsonify(computer_result)

if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)