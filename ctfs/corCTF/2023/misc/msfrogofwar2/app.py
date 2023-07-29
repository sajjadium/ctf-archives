from flask import Flask, request
from flask_socketio import SocketIO, emit
from stockfish import Stockfish
import random
import os

import chesslib
import movegen

games = {}

toxic_msges = [
    "?",
    "rip bozo",
    "so bad lmfaoo",
    "ez",
    "skill issue",
    "mad cuz bad",
    "hold this L",
    "L + ratio + you fell off",
    "i bet your main category is stego",
    "have you tried alt+f4?",
    "🤡🤡🤡"
]

win_msges = [
    "lmaooooooooo ur so bad",
    "was that it?",
    "zzzzzzzzzzzzzzzzzzzzzz",
    "hopefully the next game wont be so quick",
    "nice try - jk that was horrible",
    "this aint checkers man"
]

TURN_LIMIT = 20
STOCKFISH_DEPTH = 21
FLAG = os.environ.get("FLAG", "corctf{test_flag}")

class GameWrapper:
    def __init__(self, emit):
        self.emit = emit
        self.game = chesslib.Game(chesslib.STARTING_FEN)
        self.engine = Stockfish("./stockfish/stockfish-ubuntu-x86-64-avx2", parameters={"Threads": 4}, depth=STOCKFISH_DEPTH)

    def get_player_state(self):
        moves = [f"{m}" for m in self.game.get_moves()] if self.game.turn == chesslib.Piece.WHITE and self.game.turns < TURN_LIMIT else []

        status = self.game.get_winner()
        if self.game.turns >= TURN_LIMIT:
            status = "turn limit"

        return {
            "pos": self.game.export_fen(),
            "moves": moves,
            "your_turn": self.game.turn == chesslib.Piece.WHITE,
            "status": status,
            "turn_counter": f"{self.game.turns} / {TURN_LIMIT} turns"
        }

    def play_move(self, move):
        if self.game.turn != chesslib.Piece.WHITE:
            return
        if self.game.turns >= TURN_LIMIT:
            return

        move = movegen.Move.from_uci(self.game, move)
        legal_moves = self.game.get_moves()

        if move not in legal_moves:
            return

        self.game.play_move(move)
        self.emit("state", self.get_player_state())

        # check for winner
        status = self.game.get_winner()
        if status == chesslib.GameStatus.DRAW:
            self.emit("chat", {"name": "🐸", "msg": "Nice try... but not good enough 🐸"})
            return
        elif status == chesslib.GameStatus.WHITE_WIN:
            self.emit("chat", {"name": "🐸", "msg": "how??????"})
            self.emit("chat", {"name": "System", "msg": FLAG})
            return

        # stockfish has a habit of crashing
        # The following section is used to try to resolve this
        opponent_move, attempts = None, 0
        while not opponent_move and attempts <= 10:
            try:
                attempts += 1
                self.engine.set_fen_position(self.game.export_fen())
                opponent_move = self.engine.get_best_move(30000, 30000)
            except:
                self.engine = Stockfish("./stockfish/stockfish-ubuntu-x86-64-avx2", parameters={"Threads": 4}, depth=STOCKFISH_DEPTH)

        if opponent_move != None:
            opponent_move = movegen.Move.from_uci(self.game, opponent_move)
            if opponent_move.is_capture(self.game):
                self.emit("chat", {"name": "🐸", "msg": random.choice(toxic_msges)})
            self.game.play_move(opponent_move)
            self.emit("state", self.get_player_state())

            # check for winner
            status = self.game.get_winner()
            if status == chesslib.GameStatus.DRAW:
                self.emit("chat", {"name": "🐸", "msg": "Nice try... but not good enough 🐸"})
            elif status == chesslib.GameStatus.BLACK_WIN:
                self.emit("chat", {"name": "🐸", "msg": random.choice(win_msges)})
            
            if self.game.turns >= TURN_LIMIT:
                self.emit("chat", {"name": "🐸", "msg": random.choice(win_msges)})
        else:
            self.emit("chat", {"name": "System", "msg": "An error occurred, please restart"})

app = Flask(__name__, static_url_path='', static_folder='static')
socketio = SocketIO(app, cors_allowed_origins=[
    'https://msfrogofwar2.be.ax',
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'http://127.0.0.1:5000',
    'http://localhost:5000'
])

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'max-age=604800'
    return response

@app.route('/')
def index_route():
    return app.send_static_file('index.html')

@socketio.on('connect')
def on_connect(_):
    games[request.sid] = GameWrapper(emit)
    emit('state', games[request.sid].get_player_state())

@socketio.on('disconnect')
def on_disconnect():
    if request.sid in games:
        del games[request.sid]

@socketio.on('move')
def onmsg_move(move):
    games[request.sid].play_move(move)