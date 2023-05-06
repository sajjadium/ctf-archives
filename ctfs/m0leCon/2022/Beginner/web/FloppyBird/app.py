from flask import Flask, request, send_file, jsonify
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
import sqlite3
import os

db = sqlite3.connect('db.sqlite3', check_same_thread=False)
db.execute('CREATE TABLE IF NOT EXISTS scores (token TEXT, score INTEGER)')
app = Flask(
    __name__,
    static_url_path='',
    static_folder=os.getcwd() + '/client'
)
limiter = Limiter(app, key_func=get_remote_address)
flag = os.getenv('FLAG', 'ptm{flag}')


@app.route('/', methods=['GET'])
def home():
    return send_file('client/index.html')


@app.route('/get-token', methods=['GET'])
def get_token():
    token = os.urandom(16).hex()
    db.execute('INSERT INTO scores VALUES (?, ?)', (token, 0))
    db.commit()
    return {'ok': True, 'token': token}


@app.route('/update-score', methods=['POST'])
@limiter.limit('12/second', on_breach=lambda _: jsonify({'ok': False, 'error': 'Too many requests'}))
def update_score():
    if not request.json or 'token' not in request.json:
        return {'ok': False, 'error': 'No token was given, you need to get one if you want to play'}, 400
    client_score = request.json['score']

    if type(client_score) != int:
        return {'ok': False, 'error': 'Invalid score type, did you pass a correct number?'}
    elif type(request.json['token']) != str:
        return {'ok': False, 'error': 'Invalid token type, did you pass the correct token?'}
    db_score = db.execute(
        'SELECT score FROM scores WHERE token = ?',
        (request.json['token'],)
    ).fetchone()

    if db_score is None:
        return {'error': 'The given token is invalid, did I ever see you before?'}, 400
    db_score = db_score[0]

    if client_score == db_score + 1 or client_score == db_score * 2:
        db.execute(
            'UPDATE scores SET score = ? WHERE token = ?',
            (client_score, request.json['token'])
        )
    elif client_score > db_score:
        return {'ok': False, 'error': 'An invalid score was given, are you trying to hack me?'}, 400

    if client_score >= 1000:
        return {'ok': True, 'flag': flag}, 200
    return {'ok': True}, 200
