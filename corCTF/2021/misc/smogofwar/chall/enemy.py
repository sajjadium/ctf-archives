import chess
import random
from stockfish import Stockfish
import os

FLAG = os.getenv("FLAG")
STOCKFISHTIME = int(float(os.getenv("STOCKFISHTIME"))*1000)

toxic_msges = [
    "so bad lmfaoo",
    "pepega clap wr",
    "ez",
    "are you paying attention?",
    "man being a computer is so nice",
    "mad cuz bad",
    "hold this L",
    "L nerd",
    "iq = elo = 0",
    "i bet your main category is steg",
    "have you tried alt+f4?",
    "this aint checkers man"
]

win_msges = [
    "don't waste my time",
    "was that it?",
    "zzzzzzzzzzzzzzzzzzzzzz",
    "LLLLLLLLLLLLLLLLLLLLLLLL",
    "hopefully the next game wont be so quick"
]

class Enemy:
    def __init__(self, fen, emit):
        self.internal_board = chess.Board(fen)
        self.emit = emit
        self.stockfish = Stockfish("./stockfish_14_linux_x64_avx2/stockfish_14_x64_avx2", parameters={"Threads": 4})
        self.quit = False

    def get_moves(self):
        moves = self.internal_board.pseudo_legal_moves
        return [m.uci() for m in moves]

    def is_valid_move(self, move):
        return move in self.get_moves()

    def chat(self, msg):
        self.emit("chat", {"name": "Bot", "msg": msg})

    def play_move(self, move):
        if self.quit:
            return

        if not self.is_valid_move(move):
            self.quit = True
            self.chat("hey... wait a second...")
            return

        move = chess.Move.from_uci(move)
        self.internal_board.push(move)

    def lemonthink(self, move):
        self.play_move(move)

    def check_for_win_condition(self):
        new_board = self.internal_board.copy()
        new_board.turn = chess.WHITE

        if new_board.is_check():
            for m in self.internal_board.pseudo_legal_moves:
                if self.internal_board.is_capture(m) and m.to_square == self.internal_board.king(chess.WHITE):
                    return m.uci()

        return False

    def normalthink(self, possible_moves):
        if self.quit:
            return

        if self.check_for_win_condition():
            self.chat(random.choice(win_msges))
            return self.check_for_win_condition()

        try:
            self.stockfish.set_fen_position(self.internal_board.fen())
        except:
            self.quit = True
            self.chat("uhh... my brain broke hol up")

        if sorted(self.get_moves()) != sorted(possible_moves):
            self.quit = True
            self.chat("hey... wait a second...")
            return

        best_move = None
        try:
            best_move = self.stockfish.get_best_move_time(10000)
        except:
            self.quit = True
            self.chat("uhh... my brain broke hol up")

        if best_move is None:
            best_move = random.choice(possible_moves)

        if best_move not in possible_moves:
            self.quit = True
            self.chat("hey... wait a second...")
            return

        if self.internal_board.is_capture(chess.Move.from_uci(best_move)):
            self.chat(random.choice(toxic_msges))

        self.play_move(best_move)
        return best_move

    def resign(self):
        if self.quit:
            return

        self.chat("damn, how did you do that???")
        self.chat(FLAG)
