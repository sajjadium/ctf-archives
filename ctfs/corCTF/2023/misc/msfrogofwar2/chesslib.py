class Piece:
    NONE = None
    KING = 0
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5

    KIND_MASK = 7

    WHITE = 8
    BLACK = 16

    COLOR_MASK = 24

    def color(piece):
        return piece & Piece.COLOR_MASK

    def kind(piece):
        return piece & Piece.KIND_MASK
    
    def to_symbol(piece, default=" "):
        if piece != Piece.NONE:
            return PIECE_SYMBOLS.get(PIECE_TO_CHAR.get(piece, "?"), "?")
        else:
            return default
    
    def to_char(piece, default=" "):
        if piece != Piece.NONE:
            return PIECE_TO_CHAR.get(piece, "?")
        else:
            return default

CHAR_TO_PIECE = {
    "k": Piece.BLACK | Piece.KING,
    "p": Piece.BLACK | Piece.PAWN,
    "n": Piece.BLACK | Piece.KNIGHT,
    "b": Piece.BLACK | Piece.BISHOP,
    "r": Piece.BLACK | Piece.ROOK,
    "q": Piece.BLACK | Piece.QUEEN,

    "K": Piece.WHITE | Piece.KING,
    "P": Piece.WHITE | Piece.PAWN,
    "N": Piece.WHITE | Piece.KNIGHT,
    "B": Piece.WHITE | Piece.BISHOP,
    "R": Piece.WHITE | Piece.ROOK,
    "Q": Piece.WHITE | Piece.QUEEN, 
}
PIECE_TO_CHAR = {v: k for k, v in CHAR_TO_PIECE.items()}

PIECE_SYMBOLS = {
    "r": "♖", "R": "♜",
    "n": "♘", "N": "♞",
    "b": "♗", "B": "♝",
    "q": "♕", "Q": "♛",
    "k": "♔", "K": "♚",
    "p": "♙", "P": "♟",
}

class CastlingRights:
    NONE = 0
    WHITE_KING = 1
    WHITE_QUEEN = 2
    BLACK_KING = 4
    BLACK_QUEEN = 8

class Position:
    def __init__(self, rank, file):
        self.rank = rank
        self.file = file
    
    def from_uci(coord):
        return Position(int(coord[1]) - 1, int("abcdefgh".index(coord[0])))
    
    def from_index(index):
        return Position(index // 8, index % 8)

    def to_index(self):
        return self.rank * 8 + self.file

    def __eq__(a, b):
        return a and b and a.rank == b.rank and a.file == b.file

    def __repr__(self):
        return f"{[c for c in 'abcdefgh'][self.file]}{self.rank + 1}"

class Board:
    def __init__(self):
        self.squares = [Piece.NONE] * 64

    def load_board_fen(self, board_fen):
        file, rank = 0, 7
        for c in board_fen:
            if c == '/':
                file = 0
                rank -= 1
            elif c.isdigit():
                file += int(c)
            else:
                self.squares[rank * 8 + file] = CHAR_TO_PIECE[c]
                file += 1

    def at(self, rank_or_pos, file = None):
        if isinstance(rank_or_pos, Position):
            return self.squares[rank_or_pos.to_index()]
        return self.squares[rank_or_pos * 8 + file]
    
    def play_move(self, move, turn):
        piece = self.at(move.start)

        start_index = move.start.to_index()
        end_index = move.end.to_index()

        self.squares[end_index] = piece
        self.squares[start_index] = Piece.NONE

        if move.castle != None:
            # play rook move stored in castle field
            self.play_move(move.castle, turn)

        if move.en_passant != None:
            # capture pawn stored in en_passant field
            self.squares[move.en_passant.to_index()] = Piece.NONE

        if move.promotion != Piece.NONE:
            # change piece to be the one stored in the promotion field
            self.squares[end_index] = move.promotion | turn

    def __repr__(self):
        output = []
        for rank in range(7, -1, -1):
            line = ""
            for file in range(7, -1, -1):
                line += Piece.to_symbol(self.at(rank, file))
            output.append(line[::-1])
        return "\n".join(output)

class GameStatus:
    RUNNING = "running"
    DRAW = "draw"
    WHITE_WIN = "white win"
    BLACK_WIN = "black win"

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

import movegen
class Game:
    def __init__(self, fen):
        board_fen, turn, castling_rights, en_passant, _, move_counter = fen.split(" ")
        self.board = Board()
        self.board.load_board_fen(board_fen)
        self.turn = {"w": Piece.WHITE, "b": Piece.BLACK}[turn]
        self.turns = int(move_counter)

        self.castling_rights = CastlingRights.NONE
        for c in castling_rights:
            if c == "-": break
            if c.lower() == "q":
                self.castling_rights |= CastlingRights.BLACK_QUEEN if c.islower() else CastlingRights.WHITE_QUEEN
            elif c.lower() == "k":
                self.castling_rights |= CastlingRights.BLACK_KING if c.islower() else CastlingRights.WHITE_KING
        
        if en_passant == "-":
            self.en_passant = None
        else:
            self.en_passant = Position.from_uci(en_passant)

    def copy(self):
        return Game(self.export_fen())

    def play_move(self, move):
        piece = self.board.at(move.start)
        target = self.board.at(move.end)

        self.board.play_move(move, self.turn)
        if Piece.kind(piece) == Piece.KING:
            # remove castling rights
            if self.turn == Piece.WHITE:
                self.castling_rights &= ~(CastlingRights.WHITE_KING | CastlingRights.WHITE_QUEEN)
            else:
                self.castling_rights &= ~(CastlingRights.BLACK_KING | CastlingRights.BLACK_QUEEN)
        elif Piece.kind(piece) == Piece.ROOK:
            # remove castling rights for only one side
            if move.start.file == 0:
                self.castling_rights &= ~(CastlingRights.WHITE_QUEEN if self.turn == Piece.WHITE else CastlingRights.BLACK_QUEEN)
            elif move.start.file == 7:
                self.castling_rights &= ~(CastlingRights.WHITE_KING if self.turn == Piece.WHITE else CastlingRights.BLACK_KING)
    
        if Piece.kind(piece) == Piece.PAWN and move.pawn_push:
            # if double move, set en passant flag
            self.en_passant = move.pawn_push
        else:
            self.en_passant = None

        # if someone captures your rook, you lose castling rights for that rook
        if target != Piece.NONE and Piece.kind(target) == Piece.ROOK:
            if move.end.file == 0:
                self.castling_rights &= ~(CastlingRights.BLACK_QUEEN if self.turn == Piece.WHITE else CastlingRights.WHITE_QUEEN)
            elif move.end.file == 7:
                self.castling_rights &= ~(CastlingRights.BLACK_KING if self.turn == Piece.WHITE else CastlingRights.WHITE_KING)

        self.swap_turn()

        # once white and black have both played, one turn has passed
        if self.turn == Piece.WHITE:
            self.turns += 1

    def get_moves(self):
        return movegen.get_legal_moves(self)

    def get_winner(self):
        possible_moves = self.get_moves()
        # if there are possible moves left, the game is not over
        if len(possible_moves) != 0:
            return GameStatus.RUNNING
        # now, we check whether the king is in check
        self.swap_turn() # swap turn to enemy side to get attacking squares
        danger_squares = movegen.get_danger_squares(self)
        self.swap_turn()
        if movegen.king_in_danger(self, danger_squares):
            # if king is in danger, then the current player lost
            return {Piece.BLACK: GameStatus.WHITE_WIN, Piece.WHITE: GameStatus.BLACK_WIN}[self.turn]
        # else, king is not in danger, but no moves are left, so we are in stalemate
        return GameStatus.DRAW

    def swap_turn(self):
        self.turn = {Piece.BLACK: Piece.WHITE, Piece.WHITE: Piece.BLACK}[self.turn]

    def export_fen(self):
        board_fen = []
        for rank in range(7, -1, -1):
            rank_fen = ""
            empty_counter = 0
            for file in range(8):
                piece = self.board.at(rank, file)
                if piece == Piece.NONE:
                    empty_counter += 1
                    continue
                if empty_counter != 0:
                    rank_fen += str(empty_counter)
                    empty_counter = 0
                rank_fen += Piece.to_char(piece)
            if empty_counter != 0:
                rank_fen += str(empty_counter)
            board_fen.append(rank_fen)
        board_fen = "/".join(board_fen)
        
        turn = {Piece.WHITE: "w", Piece.BLACK: "b"}[self.turn]

        castling_rights = ""
        if self.castling_rights & CastlingRights.WHITE_KING:
            castling_rights += "K"
        if self.castling_rights & CastlingRights.WHITE_QUEEN:
            castling_rights += "Q"
        if self.castling_rights & CastlingRights.BLACK_KING:
            castling_rights += "k"
        if self.castling_rights & CastlingRights.BLACK_QUEEN:
            castling_rights += "q"
        castling_rights = castling_rights or "-"

        en_passant = self.en_passant or "-"

        return f"{board_fen} {turn} {castling_rights} {en_passant} 0 {self.turn}"

    def __repr__(self):
        return f"Board:\n{self.board}\nTurn: {self.turn}\nCastling rights: {self.castling_rights}\nEn passant: {self.en_passant}"