from flask import Flask, render_template, jsonify, request
import json
import secrets
import random
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

app = Flask(__name__)

# Game configuration
GRID_SIZE = 20  # 20x20 grid
SNAKE_SLEEP_SCORE = 100  # Snake gets tired and sleeps at this score
MAX_FLAG_SCORE = 999  # Need this score for flag
FLAG = os.getenv("FLAG")


SECRET_KEY = os.urandom(32)  # 32 bytes for AES-256

def aes_encrypt(data_bytes, key):
    nonce = get_random_bytes(8)
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    ciphertext = cipher.encrypt(data_bytes)
    return nonce + ciphertext

def aes_decrypt(encrypted_data, key):
    nonce = encrypted_data[:8]
    ciphertext = encrypted_data[8:]
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    
    return plaintext

def create_score_token(score, player_id):

    token_data = {
        "score": score,
        "playerId": player_id
    } 
    json_str = json.dumps(token_data)
    json_bytes = json_str.encode('utf-8')
    
    encrypted = aes_encrypt(json_bytes, SECRET_KEY)

    return encrypted.hex()

def generate_food_position():
    """
    Generate a random food position on the grid
    """
    x = random.randint(0, GRID_SIZE - 1)
    y = random.randint(0, GRID_SIZE - 1)
    return {'x': x, 'y': y}

def validate_score_token(token_hex):
    """
    Validate and decrypt a score token
    Returns (score, player_id, error_message) tuple
    """
    try:
        encrypted_bytes = bytes.fromhex(token_hex)
        decrypted_bytes = aes_decrypt(encrypted_bytes, SECRET_KEY)

        try:
            json_str = decrypted_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return None, None, "Bad token: invalid UTF-8"
        if any(ord(c) < 32 and c not in '\n\r\t' or ord(c) > 126 for c in json_str):
            return None, None, "Bad token: contains non-printable characters"

        try:
            token_data = json.loads(json_str)
        except json.JSONDecodeError as e:
            return None, None, f"Bad token: invalid JSON - {str(e)}"
        
        if 'score' not in token_data or 'playerId' not in token_data:
            return None, None, "Bad token: missing fields"
        
        score = token_data['score']
        player_id = token_data['playerId']
        
        if not isinstance(score, int) or score < 0:
            return None, None, "Bad token: invalid score"
        
        return score, player_id, None
        
    except Exception as e:
        return None, None, f"Bad token: {str(e)}"

@app.route('/')
def home():
    """Home page route"""
    return render_template('home.html')

@app.route('/game')
def game():
    """Game page route"""
    return render_template('game.html')

@app.route('/scoreboard')
def scoreboard():
    """Scoreboard page route"""
    return render_template('scoreboard.html')

@app.route('/api/scores')
def get_scores():
    """API endpoint to get scores"""
    dummy_scores = [
        {"name": "Gianlu Prime", "score": 420, "date": "2025-4-20"},
        {"name": "Carmelo", "score": "104+1", "date": "2025-4-20"},
        {"name": "Schrody", "score": 104, "date": "2025-4-20"},
    ]
    return jsonify(dummy_scores)

@app.route('/api/game/start', methods=['POST'])
def start_game():
    """Initialize a new game session - returns player ID and initial food"""
        
    player_id = secrets.token_hex(8)
    
    initial_food = generate_food_position()
    
    print(f"DEBUG: Game started for player {player_id}")
    print(f"DEBUG: Initial food: {initial_food}")
    
    return jsonify({
        'success': True,
        'playerId': player_id,
        'food': initial_food  
    })

@app.route('/api/game/food', methods=['POST'])
def food_eaten():
    """
    Called when player eats food - increments score and generates new food
    """
    data = request.get_json()
    
    if not data or 'playerId' not in data:

        return jsonify({'error': 'Missing required fields', 'required': ['playerId']}), 400
    
    player_id = data['playerId']

    current_score = 0
    if 'scoreToken' in data and data['scoreToken']:
        score, token_player_id, error = validate_score_token(data['scoreToken'])
        if error:
            return jsonify({'error': 'Invalid score token', 'message': error}), 400
        
        if token_player_id != player_id:
            return jsonify({'error': 'Token does not match player ID'}), 403
        
        current_score = score

    new_score = current_score + 10

    if new_score >= SNAKE_SLEEP_SCORE:
        new_score = SNAKE_SLEEP_SCORE  

        score_token = create_score_token(new_score, player_id)
        
        return jsonify({
            'success': True,
            'snake_sleeping': True,  
            'scoreToken': score_token,
            'score': new_score,
            'message': 'The snake is tired and needs to sleep!',
        })
    
    new_food = generate_food_position()
    score_token = create_score_token(new_score, player_id)
    
    return jsonify({
        'success': True,
        'scoreToken': score_token,
        'newFood': new_food,  
        'score': new_score
    })

@app.route('/api/submit-score', methods=['POST'])
def submit_score():
    """API endpoint to submit a final score using the encrypted token"""
    try:
        data = request.get_json() 
        if not data or 'scoreToken' not in data or 'playerName' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        player_name = data['playerName'].strip()
        score_token = data['scoreToken'] 
        if not player_name or len(player_name) > 50:
            return jsonify({'error': 'Invalid player name'}), 400

        score, player_id, error = validate_score_token(score_token)
        
        if error:
            return jsonify({
                'error': 'Invalid score token',
                'message': error
            }), 400

        response_data = {
            'success': True,
            'message': 'Score submitted successfully!',
            'data': {
                'name': player_name,
                'score': score,
            }
        }
        
        # Check if score qualifies for the flag
        if score >= MAX_FLAG_SCORE:
            response_data['flag'] = FLAG
            response_data['message'] = 'How did you manage to get such a high score? You cheated again right?'
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)