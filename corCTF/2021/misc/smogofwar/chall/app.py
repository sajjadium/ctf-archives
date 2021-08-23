from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

import game

app = Flask(__name__, static_url_path='', static_folder='static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index_route():
    return app.send_static_file('index.html')

@socketio.on('connect')
def on_connect():
    game.start(request.sid, emit)
    emit('state', game.get(request.sid).get_player_state())

@socketio.on('disconnect')
def on_disconnect():
    game.destroy(request.sid)

@socketio.on('move')
def onmsg_move(move):
    game.get(request.sid).player_move(move)