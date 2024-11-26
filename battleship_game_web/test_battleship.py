import unittest
import pickle
from app import app
from battleship_logic import BattleshipGame
 
 
class TestBattleshipApp(unittest.TestCase):
    def setUp(self):
        # Configure the Flask test client
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_key'
        self.client = app.test_client()
    
    def test_start_game(self):
        # Mock grid size
        grid_size = 8 # Must be
        response = self.client.post('/start_game', data={'grid_size': grid_size})
        
        # Check the response status code
        self.assertEqual(response.status_code, 200)
        
        # Check that the session contains the game object
        with self.client.session_transaction() as session:
            self.assertIn('game', session)
            game = pickle.loads(session['game'])
            self.assertIsInstance(game, BattleshipGame)
            self.assertEqual(len(game.player_board), grid_size)
            self.assertEqual(len(game.player_board[0]), grid_size)
        
        # Check that the rendered template contains grid size
        self.assertIn(str(grid_size), response.data.decode('utf-8'))
 
if __name__ == '__main__':
    unittest.main()
 
 