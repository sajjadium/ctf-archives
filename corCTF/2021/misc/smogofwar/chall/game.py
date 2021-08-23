import chess
from stockfish import Stockfish

from enemy import Enemy

games = {}

class Game:
    def __init__(self, emit):
        self.board = chess.Board(chess.STARTING_FEN)
        self.emit = emit
        self.enemy = Enemy(self.board.fen(), emit)

    def get_turn(self):
        return self.board.turn

    def get_moves(self):
        return self.get_side_moves(self.get_turn())

    def get_side_moves(self, side):
        new_board = self.board.copy()
        new_board.turn = side
        # technically this doesn't have all of the moves possible for fog of war chess
        # but this is SMOG of war chess, so it's definitely a different gamemode
        # yeah :)
        moves = new_board.pseudo_legal_moves
        return [m.uci() for m in moves]

    # extra info to since pawns can move diagonally only on attacks
    def get_pawn_attacks(self, side):
        pawns = self.board.pieces(chess.PAWN, side)
        squares = chess.SquareSet()
        for p in pawns:
            squares |= self.board.attacks(p)
        return [chess.square_name(s) for s in list(squares)]

    def is_player_turn(self):
        return self.get_turn() == chess.WHITE and self.board.king(chess.WHITE) is not None

    def get_player_state(self):
        return {
            "pos": self.fog_of_war(),
            "moves": self.get_side_moves(chess.WHITE),
            "pawn_attacks": self.get_pawn_attacks(chess.WHITE),
            "your_turn": self.is_player_turn(),
            "game_over": self.is_game_over()
        }

    def is_game_over(self):
        return self.board.king(chess.WHITE) is None or self.board.king(chess.BLACK) is None or self.enemy.quit

    def is_valid_move(self, move):
        return move in self.get_moves()

    def play_move(self, move):
        if self.is_game_over() or not self.is_valid_move(move):
            return False

        self.board.push(chess.Move.from_uci(move))
        return True

    def player_move(self, data):
        if self.get_turn() != chess.WHITE or self.is_game_over():
            return

        m0 = data
        m1 = data

        if isinstance(data, dict) and "_debug" in data:
            m0 = data["move"]
            m1 = data["move2"]

        if not self.play_move(m0):
            self.emit("chat", {"name": "System", "msg": "Invalid move"})
            return

        self.emit('state', self.get_player_state())    

        if self.board.king(chess.BLACK) is None:
            self.enemy.resign()
            return

        self.enemy.lemonthink(m1) 

        enemy_move = self.enemy.normalthink(self.get_moves())
        self.play_move(enemy_move)

        self.emit('state', self.get_player_state())

    def fog_of_war(self, side=chess.WHITE):
        if self.is_game_over():
            return self.board.fen()

        new_board = self.board.copy()
        new_board.turn = side

        moves = new_board.pseudo_legal_moves
        pieces = new_board.piece_map()

        capturable = []
        for m in moves:
            if new_board.is_capture(m):
                capturable.append(m.to_square)

        pieces = {k:v for (k,v) in pieces.items() if v.color == side or k in capturable}
        new_board = chess.Board()
        new_board.set_piece_map(pieces)
        return new_board.fen()

def start(id, emit):
    games[id] = Game(emit)
    return games[id]

def destroy(id):
    if id in games:
        del games[id]

def get(id):
    return games[id]