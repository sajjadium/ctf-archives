from chesslib import Piece, Position, CastlingRights, CHAR_TO_PIECE, PIECE_TO_CHAR

class Move:
    def __init__(self, start, end, **kwargs):
        self.start = start
        self.end = end

        self.promotion = kwargs.get("promotion", Piece.NONE)
        self.castle = kwargs.get("castle", None)
        self.en_passant = kwargs.get("en_passant", None)
        self.pawn_push = kwargs.get("pawn_push", None)

    def is_legal(self, game):
        piece = game.board.at(self.start)

        # if this is castling we have to check that:
        # a) the king is not currently in check
        # b) the king does not pass through squares in check
        if self.castle:
            game.swap_turn() # swap turn to enemy side to get attacking squares
            danger_squares = get_danger_squares(game)
            game.swap_turn()

            # a) you can't castle while in check
            if self.start in danger_squares:
                return False

            # b) if castling, check if path is clear of enemy attacks
            # get direction the king moves
            sign = 1 if self.start.file < self.end.file else -1
            game.swap_turn() # swap turn to enemy side to get attacking squares
            game.board.squares[self.start.to_index()] = Piece.NONE # remove the king before checking for danger squares
            danger_squares = get_danger_squares(game)
            game.swap_turn() # revert turn swap
            game.board.squares[self.start.to_index()] = piece # place king back

            # check all spaces the king moves
            for file in range(self.start.file + sign, self.end.file + sign, sign):
                if Position(self.start.rank, file) in danger_squares:
                    return False

        # if the moving piece is a king,
        # we need to check whether the king would be attacked on that destination
        # so, we move the king to that square and check if it is in danger
        if Piece.kind(piece) == Piece.KING:
            prev_squares = game.board.squares.copy() # save board state
            game.board.squares[self.start.to_index()] = Piece.NONE # remove the king before checking for all danger squares
            game.swap_turn() # swap turn to enemy side to get attacking squares
            danger_squares = get_danger_squares(game)
            game.swap_turn() # revert turn swap
            game.board.squares[self.end.to_index()] = piece # place king on target square
            
            # check if the king would be attacked on that square
            in_danger = king_in_danger(game, danger_squares)
            game.board.squares = prev_squares # revert board state
            return not in_danger

        # non-king moves are legal if:
        # a) the piece is not pinned or
        # b) the piece is pinned but it moves along the ray aligned with the king
        # to check this, we play the move, and see if the king appears in the danger squares
        # this modifies a lot of game state, so we have to make a copy of the game
        temp_game = game.copy()
        temp_game.board.play_move(self, game.turn)
        temp_game.swap_turn()
        danger_squares = get_danger_squares(temp_game)

        return not king_in_danger(game, danger_squares)

    def from_uci(game, uci):
        move = Move(Position.from_uci(uci[0:2]), Position.from_uci(uci[2:4]))
        piece = game.board.at(move.start)
        
        # if pawn promotion on last rank, set promotion flag
        if Piece.kind(piece) == Piece.PAWN \
            and len(uci) == 5:
            target_kind = Piece.kind(CHAR_TO_PIECE[uci[4]])
            move.promotion = move.end.rank == {Piece.WHITE: 7, Piece.BLACK: 0}[game.turn] and target_kind

        # if double pawn push, set pawn push flag
        if Piece.kind(piece) == Piece.PAWN \
            and abs(move.start.rank - move.end.rank) == 2:
            move.pawn_push = Position(min(move.start.rank, move.end.rank) + 1, move.start.file)

        # if en passant, set en passant flag
        if Piece.kind(piece) == Piece.PAWN \
            and game.en_passant and game.en_passant == move.end:
            # set en passant flag to delete the correct pawn
            move.en_passant = Position(move.start.rank, move.end.file)

        # if castling, set castling flag
        # check for both king and queen side castling
        queen_side = CastlingRights.WHITE_QUEEN if game.turn == Piece.WHITE else CastlingRights.BLACK_QUEEN
        if Piece.kind(piece) == Piece.KING \
            and game.castling_rights & queen_side \
            and move.end == Position(0 if game.turn == Piece.WHITE else 7, 2):
            rook_pos = (0 if game.turn == Piece.WHITE else 7, 0)
            move.castle = Move(Position(*rook_pos), Position(rook_pos[0], rook_pos[1] + 3))

        king_side = CastlingRights.WHITE_KING if game.turn == Piece.WHITE else CastlingRights.BLACK_KING
        if Piece.kind(piece) == Piece.KING \
            and game.castling_rights & king_side \
            and move.end == Position(0 if game.turn == Piece.WHITE else 7, 6):
            rook_pos = (0 if game.turn == Piece.WHITE else 7, 7)
            move.castle = Move(Position(*rook_pos), Position(rook_pos[0], rook_pos[1] - 2))

        return move

    def is_capture(self, game):
        target = game.board.at(self.end)
        if target != Piece.NONE:
            return True
        # we need to check for en passant since the pawn does not capture on its end square
        if self.en_passant != None:
            return True
        return False

    def __repr__(self):
        if self.promotion:
            target = { Piece.QUEEN: "q", Piece.KNIGHT: "n", Piece.BISHOP: "b", Piece.ROOK: "r"}[self.promotion]
            return f"{self.start}{self.end}{target}"
        return f"{self.start}{self.end}"
    
    def __eq__(a, b):
        return a and b and a.start == b.start and a.end == b.end

def king_in_danger(game, danger_squares):
    # loop through board to look for king
    for index, piece in enumerate(game.board.squares):
        if piece == Piece.KING | game.turn:
            king_pos = Position.from_index(index)
            if king_pos not in danger_squares:
                return False

    # else, king is in danger
    return True

def get_legal_moves(game):
    return [m for m in get_pseudo_legal_moves(game) if m.is_legal(game)]

def get_pseudo_legal_moves(game):
    moves = []
    for rank in range(8):
        for file in range(8):
            moves += get_moves_for(game, rank, file)
    return moves

def get_danger_squares(game):
    moves = []
    for rank in range(8):
        for file in range(8):
            moves += get_moves_for(game, rank, file, True)
    return [m.end for m in moves]

def get_moves_for(game, rank, file, danger_calc=False):
    piece = game.board.at(rank, file)
    
    # no moves for this piece if the square is empty or it's of the wrong color
    if piece == Piece.NONE or Piece.color(piece) != game.turn:
        return []

    kind = Piece.kind(piece)
    if kind == Piece.PAWN:
        return get_pawn_moves(game, rank, file, danger_calc)
    elif kind == Piece.KNIGHT:
        return get_knight_moves(game, rank, file, danger_calc)
    elif kind == Piece.BISHOP:
        return get_bishop_moves(game, rank, file, danger_calc)
    elif kind == Piece.ROOK:
        return get_rook_moves(game, rank, file, danger_calc)
    elif kind == Piece.QUEEN:
        return get_queen_moves(game, rank, file, danger_calc)
    elif kind == Piece.KING:
        return get_king_moves(game, rank, file, danger_calc)
    
    return []

def is_valid_square(rank, file):
    return rank >= 0 and rank < 8 and file >= 0 and file < 8

def get_pawn_moves(game, rank, file, danger_calc=False):
    moves = []
    special = []
    pawn_dir = 1 if game.turn == Piece.WHITE else -1
    start = Position(rank, file)

    def promote(rank, file):
        special.append(Move(start, Position(rank, file), promotion=Piece.KNIGHT))
        special.append(Move(start, Position(rank, file), promotion=Piece.BISHOP))
        special.append(Move(start, Position(rank, file), promotion=Piece.ROOK))
        special.append(Move(start, Position(rank, file), promotion=Piece.QUEEN))

    # move 1 square forward
    if not danger_calc and is_valid_square(rank + pawn_dir, file) and game.board.at(rank + pawn_dir, file) == Piece.NONE:
        # check for promotion
        if rank + pawn_dir == {Piece.WHITE: 7, Piece.BLACK: 0}[game.turn]:
            promote(rank + pawn_dir, file)
        else:
            moves.append((rank + pawn_dir, file))

    # move 2 squares forward, if on home row
    if not danger_calc and rank == {Piece.WHITE: 1, Piece.BLACK: 6}[game.turn] \
        and is_valid_square(rank + pawn_dir, file) and game.board.at(rank + pawn_dir, file) == Piece.NONE \
        and is_valid_square(rank + 2 * pawn_dir, file) and game.board.at(rank + 2 * pawn_dir, file) == Piece.NONE:
        special.append(Move(start, Position(rank + 2 * pawn_dir, file), pawn_push=Position(rank + pawn_dir, file)))

    # capture diagonally left and right
    for offset in [-1, 1]:
        if is_valid_square(rank + pawn_dir, file + offset):
            position = Position(rank + pawn_dir, file + offset)
            target_piece = game.board.at(rank + pawn_dir, file + offset)
            if danger_calc or (target_piece != Piece.NONE and Piece.color(target_piece) != game.turn):
                # check for promotion
                if rank + pawn_dir == {Piece.WHITE: 7, Piece.BLACK: 0}[game.turn]:
                    promote(rank + pawn_dir, file + offset)
                else:
                    moves.append((rank + pawn_dir, file + offset))
            # en passant
            elif game.en_passant and game.en_passant == position:
                target_piece = game.board.at(rank, file + offset)
                if target_piece != Piece.NONE and Piece.color(target_piece) != game.turn:
                    special.append(Move(start, position, en_passant=Position(rank, file + offset)))

    return [Move(start, Position(*end)) for end in moves] + special

def get_knight_moves(game, rank, file, danger_calc=False):
    moves = []
    offsets = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    start = Position(rank, file)

    for o in offsets:
        new_rank, new_file = rank + o[0], file + o[1]
        if is_valid_square(new_rank, new_file):
            target_piece = game.board.at(new_rank, new_file)
            
            # can move there if either no piece, or piece of opponent type
            if danger_calc or (target_piece == Piece.NONE or Piece.color(target_piece) != game.turn):
                moves.append((new_rank, new_file))

    return [Move(start, Position(*end)) for end in moves]

def get_bishop_moves(game, rank, file, danger_calc=False):
    moves = []
    offsets = [
        (1, 1), (1, -1), (-1, 1), (-1, -1)
    ]
    start = Position(rank, file)

    for o in offsets:
        new_rank, new_file = rank + o[0], file + o[1]
        # it can move in a direction until it hits some piece or goes off the edge
        while is_valid_square(new_rank, new_file) and game.board.at(new_rank, new_file) == Piece.NONE:
            moves.append((new_rank, new_file))
            new_rank, new_file = new_rank + o[0], new_file + o[1]
        # if it hits a piece, and it's on the other team, it can capture it
        if not is_valid_square(new_rank, new_file):
            continue
        target_piece = game.board.at(new_rank, new_file)
        if danger_calc or (target_piece != Piece.NONE and Piece.color(target_piece) != game.turn):
            moves.append((new_rank, new_file))

    return [Move(start, Position(*end)) for end in moves]

def get_rook_moves(game, rank, file, danger_calc=False):
    moves = []
    offsets = [
        (1, 0), (0, 1), (-1, 0), (0, -1)
    ]
    start = Position(rank, file)

    for o in offsets:
        new_rank, new_file = rank + o[0], file + o[1]
        # it can move in a direction until it hits some piece or goes off the edge
        while is_valid_square(new_rank, new_file) and game.board.at(new_rank, new_file) == Piece.NONE:
            moves.append((new_rank, new_file))
            new_rank, new_file = new_rank + o[0], new_file + o[1]
        # if it hits a piece, and it's on the other team, it can capture it
        if not is_valid_square(new_rank, new_file):
            continue
        target_piece = game.board.at(new_rank, new_file)
        if danger_calc or (target_piece != Piece.NONE and Piece.color(target_piece) != game.turn):
            moves.append((new_rank, new_file))

    return [Move(start, Position(*end)) for end in moves]

def get_queen_moves(game, rank, file, danger_calc=False):
    return get_bishop_moves(game, rank, file, danger_calc) + get_rook_moves(game, rank, file, danger_calc)

def get_king_moves(game, rank, file, danger_calc=False):
    moves = []
    offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    start = Position(rank, file)

    for o in offsets:
        new_rank, new_file = rank + o[0], file + o[1]
        if is_valid_square(new_rank, new_file):
            target_piece = game.board.at(new_rank, new_file)
            # can move there if either no piece, or piece of opponent type
            if danger_calc or (target_piece == Piece.NONE or Piece.color(target_piece) != game.turn):
                moves.append((new_rank, new_file))

    # check for castling
    queen_side = CastlingRights.WHITE_QUEEN if game.turn == Piece.WHITE else CastlingRights.BLACK_QUEEN
    king_side = CastlingRights.WHITE_KING if game.turn == Piece.WHITE else CastlingRights.BLACK_KING
    castling = []
    if not danger_calc and game.castling_rights & queen_side:
        # check that there is nothing between the king and queen-side rook
        rook_pos = (0 if game.turn == Piece.WHITE else 7, 0)
        check_pos = (rank, file - 1)

        # move check pos left until it hits rook pos
        while is_valid_square(*check_pos) and check_pos != rook_pos and game.board.at(*check_pos) == Piece.NONE:
            check_pos = (check_pos[0], check_pos[1] - 1)
        if is_valid_square(*check_pos) and check_pos == rook_pos: # nothing was in between them
            castling.append(Move(start, Position(rook_pos[0], rook_pos[1] + 2), 
                                 castle=Move(Position(*rook_pos), Position(rook_pos[0], rook_pos[1] + 3))))
    if not danger_calc and game.castling_rights & king_side:
        # check that there is nothing between the king and king-side rook
        rook_pos = (0 if game.turn == Piece.WHITE else 7, 7)
        check_pos = (rank, file + 1)
        # move check pos right until it hits rook pos
        while is_valid_square(*check_pos) and check_pos != rook_pos and game.board.at(*check_pos) == Piece.NONE:
            check_pos = (check_pos[0], check_pos[1] + 1)
        if is_valid_square(*check_pos) and check_pos == rook_pos: # nothing was in between them
            castling.append(Move(start, Position(rook_pos[0], rook_pos[1] - 1),
                                 castle=Move(Position(*rook_pos), Position(rook_pos[0], rook_pos[1] - 2))))

    return [Move(start, Position(*end)) for end in moves] + castling