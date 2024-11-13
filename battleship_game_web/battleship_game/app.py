from flask import Flask, render_template, request, jsonify, session
from battleship_logic import BattleshipGame
import pickle

app = Flask(__name__)
app.secret_key = 'battleship_dev_key_2024'  # Required for session management

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    # Create a new game instance
    game = BattleshipGame()
    grid_size = int(request.form.get('grid_size', 10))
    game.new_game(grid_size)
    
    # Store the game state in the session
    session['game'] = pickle.dumps(game)
    
    return render_template('game.html', grid_size=grid_size, player_board=game.player_board)

@app.route('/make_move', methods=['POST'])
def make_move():
    # Retrieve game state from session
    game = pickle.loads(session['game'])
    
    row = int(request.json['row'])
    col = int(request.json['col'])
    
    # Player's move
    player_result = game.make_move(row, col)
    
    # Save game state
    session['game'] = pickle.dumps(game)
    
    return jsonify({"player": player_result})

@app.route('/computer_turn', methods=['POST'])
def computer_turn():
    # Retrieve game state from session
    game = pickle.loads(session['game'])
    
    # Computer's move
    computer_result = game.computer_turn()
    
    # Save updated game state
    session['game'] = pickle.dumps(game)
    
    return jsonify(computer_result)

if __name__ == '__main__':
    app.run(debug=True)