#include <locale.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <wchar.h>
#define ROWS 8
#define COLS 8
#define DEPTH 17

const int BLACK_PAWN_START = 0 + 1;
const int WHITE_PAWN_START = ROWS - 1 - 1;
typedef enum PieceType_enum {
    Blank = 32,
    Pawn = 0x2659,
    King = 0x2654,
    Queen = 0x2655,
    Knight = 0x2658,
    Bishop = 0x2657,
    Rook = 0x2656
} PieceType;
typedef enum Color_enum {
    White = 0,
    Black = 6
} Color;
typedef struct Piece_struct {
    PieceType type;
    Color color;
} Piece;

typedef struct Move_struct {
    int from_row;
    int from_col;
    int to_row;
    int to_col;
    Piece piece;
} Move;

void printPiece(Piece p) {
    wint_t piece = p.type + p.color;
    printf("%lc", piece);
}

void printBoard(Piece** array) {
    for (int row = 0; row < ROWS; row++) {
        printf("%d|", ROWS - row);
        for (int col = 0; col < COLS; col++) {
            printPiece(array[row][col]);
            printf("|");
        }
        printf("\n");
    }
    printf(" |a|b|c|d|e|f|g|h|\n");
}

char pieceToFen(Piece piece) {
    char letter = ' ';
    switch (piece.type) {
        case Pawn:
            letter = 'P';
            break;
        case Knight:
            letter = 'N';
            break;
        case Bishop:
            letter = 'B';
            break;
        case Rook:
            letter = 'R';
            break;
        case Queen:
            letter = 'Q';
            break;
        case King:
            letter = 'K';
            break;
        default:
            letter = 'A';
    }

    if (piece.color == Black) {
        letter += 32;
    }

    return letter;
}

char* boardToFen(Piece** board, Color toMove, bool can_castle_left, bool can_castle_right) {
    const int MAX_FEN_SIZE = 88;
    char* fenString = malloc(sizeof(char) * MAX_FEN_SIZE);
    fenString[0] = '\0';

    for (int i = 0; i < ROWS; i++) {
        int blankCounter = 0;
        for (int j = 0; j < COLS; j++) {
            Piece piece = board[i][j];
            if (piece.type != Blank) {
                if (blankCounter > 0) {
                    char count = blankCounter + '0';
                    strncat(fenString, &count, 1);
                }
                char nextLetter = pieceToFen(piece);
                strncat(fenString, &nextLetter, 1);
                blankCounter = 0;
            } else {
                blankCounter++;
            }
        }
        if (blankCounter > 0) {
            char count = blankCounter + '0';
            strncat(fenString, &count, 1);
        }
        if (i != ROWS - 1) {
            char slash = '/';
            strncat(fenString, &slash, 1);
        }
    }
    strncat(fenString, (toMove == White) ? " w " : " b ", 3);
    strncat(fenString, can_castle_right ? "K" : "", 1);
    strncat(fenString, can_castle_left ? "Q" : "", 1);

    strncat(fenString, can_castle_right ? "k" : "", 1);
    strncat(fenString, can_castle_left ? "q" : "", 1);
    if (!can_castle_left && !can_castle_right) {
        strcat(fenString, "-");
    }

    strncat(fenString, " - 0 1", 7);
    return fenString;
}

void initBoard(Piece** board) {
    Piece whiteBackRank[COLS] =
        {
            {Rook, White},
            {Knight, White},
            {Bishop, White},
            {Queen, White},
            {King, White},
            {Bishop, White},
            {Knight, White},
            {Rook, White},
        };
    Piece blackBackRank[COLS] =
        {
            {Rook, Black},
            {Knight, Black},
            {Bishop, Black},
            {Queen, Black},
            {King, Black},
            {Bishop, Black},
            {Knight, Black},
            {Rook, Black},
        };
    memcpy(board[0], blackBackRank, sizeof(blackBackRank));
    memcpy(board[ROWS - 1], whiteBackRank, sizeof(whiteBackRank));
    for (int row = 0 + 2; row < ROWS - 2; row++) {
        for (int col = 0; col < COLS; col++) {
            board[row][col] = (Piece){Blank, White};
        }
    }
    for (int col = 0; col < COLS; col++) {
        board[WHITE_PAWN_START][col] = (Piece){Pawn, White};
    }
    for (int col = 0; col < COLS; col++) {
        board[BLACK_PAWN_START][col] = (Piece){Pawn, Black};
    }
}

bool outOfBounds(int row, int col) {
    return (row >= ROWS || row < 0 || col >= COLS || col < 0);
}

Move getMove(Color player, Piece** board) {
    char from[4];
    char to[4];
    printf("Location from > ");
    fgets(from, 4, stdin);
    printf("Location to > ");
    fgets(to, 4, stdin);
    if (strlen(from) != 3 || strlen(to) != 3) {
        puts("Invalid move, you must input like 'a4'.");
        return getMove(player, board);
    }
    int fromCol = from[0] - 'a';
    int toCol = to[0] - 'a';
    int fromRow = 8 - (from[1] - '0');
    int toRow = 8 - (to[1] - '0');
    if (outOfBounds(toRow, toCol) || outOfBounds(fromRow, fromCol)) {
        puts("Move location is off the board.");
        return getMove(player, board);
    }
    Piece movingPiece = board[fromRow][fromCol];
    if ((movingPiece.color != player && movingPiece.type != Blank) || movingPiece.type == Blank) {
        puts("You can only move your own pieces.");
        return getMove(player, board);
    }
    printf("Moving %s ", (movingPiece.color == Black) ? "BLACK" : "WHITE");
    printPiece(movingPiece);
    printf(" from row: %d, col: %d, TO row: %d, col: %d\n", fromRow, fromCol, toRow, toCol);
    if (fromCol == toCol && toRow == fromRow) {
        puts("You have to actually move the piece.");
        return getMove(player, board);
    }
    Move move = {fromRow, fromCol, toRow, toCol, movingPiece};
    return move;
}
bool checkPawnValid(Move move, Piece** board, bool isCapture) {
    int pawnStartRow = (move.piece.color == Black) ? BLACK_PAWN_START : WHITE_PAWN_START;
    int direction = (move.piece.color == Black) ? -1 : 1;
    int rowDiff = (move.from_row - move.to_row) * direction;
    if (move.to_col == move.from_col && !isCapture) {
        if (rowDiff == 1) {
            return true;
        } else if (rowDiff == 2 && move.from_row == pawnStartRow) {
            return true;
        }
    } else if (abs(move.to_col - move.from_col) == 1 && rowDiff == 1) {
        Color opponentColor = (move.piece.color == White) ? Black : White;
        if (isCapture) {
            return true;
        } else if (board[move.from_row][move.to_col].color == opponentColor && board[move.from_row][move.to_col].type != Blank) {
            return true;
        }
    }
    return false;
}

bool checkVertical(Move move, Piece** board) {
    if (move.to_col != move.from_col) {
        return false;
    }
    int direction = (move.from_row > move.to_row) ? -1 : 1;
    for (int cur_row = move.from_row + direction; cur_row != move.to_row; cur_row += direction) {
        if (board[cur_row][move.to_col].type != Blank) {
            return false;
        }
    }
    return true;
}

bool checkHorizontal(Move move, Piece** board) {
    if (move.to_row != move.from_row) {
        return false;
    }
    int direction = (move.from_col > move.to_col) ? -1 : 1;
    for (int cur_col = move.from_col + direction; cur_col != move.to_col; cur_col += direction) {
        if (board[move.to_row][cur_col].type != Blank) {
            return false;
        }
    }
    return true;
}

bool checkDiagonal(Move move, Piece** board) {
    int rowDiff = move.to_row - move.from_row;
    int colDiff = move.to_col - move.from_col;
    if (abs(rowDiff) != abs(colDiff)) {
        return false;
    }
    int rowDirection = (rowDiff > 0) ? 1 : -1;
    int colDirection = (colDiff > 0) ? 1 : -1;
    int cur_row = move.from_row + rowDirection;
    int cur_col = move.from_col + colDirection;
    while (true) {
        if (cur_row == move.to_row && cur_col == move.to_col) {
            break;
        }
        if (board[cur_row][cur_col].type != Blank) {
            return false;
        }
        cur_row += rowDirection;
        cur_col += colDirection;
    }
    return true;
}
bool checkRook(Move move, Piece** board, bool* castleLeft, bool* castleRight) {
    bool isValid = checkVertical(move, board) || checkHorizontal(move, board);
    if (isValid) {
        if (move.from_col == 0 && castleLeft != NULL && *castleLeft)
            *castleLeft = false;
        if ((move.from_col == COLS - 1) && castleRight != NULL && *castleRight)
            *castleRight = false;
    }
    return isValid;
}

bool checkKnight(Move move, Piece** board) {
    int rowDiff = abs(move.to_row - move.from_row);
    int colDiff = abs(move.to_col - move.from_col);
    return (rowDiff + colDiff == 3 && rowDiff > 0 && colDiff > 0);
}

bool checkKing(Move move, Piece** board, bool* castleLeft, bool* castleRight) {
    int rowDiff = abs(move.to_row - move.from_row);
    int colDiff = abs(move.to_col - move.from_col);

    if (rowDiff <= 1 && colDiff <= 1) {
        if (castleLeft != NULL && castleRight != NULL) {
            *castleLeft = false;
            *castleRight = false;
        }
        return true;
    } else {
        if (rowDiff == 0 && move.from_col == 4) {
            if (move.to_col == 6 && board[move.to_row][5].type == Blank && board[move.to_row][6].type == Blank && castleRight != NULL && *castleRight) {
                *castleLeft = false;
                *castleRight = false;
                puts("Castling to the right side (if ur white)");
                return true;
            }
            if (move.to_col == 2 && board[move.to_row][1].type == Blank && board[move.to_row][2].type == Blank && board[move.to_row][3].type == Blank && castleLeft != NULL && *castleLeft) {
                *castleLeft = false;
                *castleRight = false;
                puts("Castling to the left side (if ur white)");
                return true;
            }
            puts("Whatever king move that was, you can't actually castle");
        }
    }
    return false;
}

Move locateKing(Piece** board, Color color) {
    for (int row = 0; row < ROWS; row++) {
        for (int col = 0; col < COLS; col++) {
            if (board[row][col].type == King && board[row][col].color == color) {
                return (Move){
                    -1,
                    -1,
                    row,
                    col,
                    Blank,
                };
            }
        }
    }
}
bool moveIsCapture(Move move, Piece** board) {
    Piece moveToSquare = board[move.to_row][move.to_col];
    bool isCapture = false;
    if (moveToSquare.type != Blank) {
        if (moveToSquare.color == move.piece.color) {
            return false;
        } else {
            isCapture = true;
        }
    }
    return isCapture;
}

bool isPsuedoLegal(Move move, Piece** board, bool* castleLeft, bool* castleRight) {
    bool isCapture = moveIsCapture(move, board);
    if (board[move.to_row][move.to_col].color == move.piece.color && board[move.to_row][move.to_col].type != Blank) {
        return false;
    }

    switch (move.piece.type) {
        case Pawn:
            return checkPawnValid(move, board, isCapture);
        case Rook:
            return checkRook(move, board, castleLeft, castleRight);
        case Queen:
            return checkVertical(move, board) || checkHorizontal(move, board) || checkDiagonal(move, board);
        case Bishop:
            return checkDiagonal(move, board);
        case Knight:
            return checkKnight(move, board);
        case King:
            return checkKing(move, board, castleLeft, castleRight);
        case Blank:
            puts("How do you even move a blank piece wut??");
            exit(99);
        default:
            puts("I covered all the cases tho??");
            exit(98);
    }
}

bool isInCheck(Piece** board, Color kingColor, Move* checkingMovePtr) {
    Move attackKingMove = locateKing(board, kingColor);

    Color opponentColor = (kingColor == White) ? Black : White;

    for (int row = 0; row < ROWS; row++) {
        for (int col = 0; col < COLS; col++) {
            if (board[row][col].color == opponentColor && board[row][col].type != Blank) {
                attackKingMove.from_col = col;
                attackKingMove.from_row = row;
                attackKingMove.piece = board[row][col];
                if (isPsuedoLegal(attackKingMove, board, NULL, NULL)) {
                    if (checkingMovePtr != NULL) {
                        *checkingMovePtr = attackKingMove;
                    }
                    return true;
                }
            }
        }
    }
    return false;
}

bool isInCheckAfter(Move move, Piece** board) {
    Piece pieceAtMoveSpot = board[move.to_row][move.to_col];
    board[move.to_row][move.to_col] = move.piece;
    board[move.from_row][move.from_col] = (Piece){Blank, White};

    bool inCheckAfter = isInCheck(board, move.piece.color, NULL);

    board[move.to_row][move.to_col] = pieceAtMoveSpot;
    board[move.from_row][move.from_col] = move.piece;

    return inCheckAfter;
}

bool isLegal(Move move, Piece** board, bool* castleLeft, bool* castleRight) {
    return isPsuedoLegal(move, board, castleLeft, castleRight) && !isInCheckAfter(move, board);
}

bool isCheckmate(Move checkingMove, Piece** board) {
    Color playerColor = (checkingMove.piece.color == White) ? Black : White;

    Move blockingCheckMove;
    if (checkingMove.piece.type != Knight && checkingMove.piece.type != Pawn) {
        int rowDirection = checkingMove.to_row - checkingMove.from_row;
        int colDirection = checkingMove.to_col - checkingMove.from_col;
        if (rowDirection != 0) {
            rowDirection /= abs(rowDirection);
        }
        if (colDirection != 0) {
            colDirection /= abs(colDirection);
        }
        int curRowPos = checkingMove.from_row + rowDirection;
        int curColPos = checkingMove.from_col + colDirection;
        while (true) {
            if (curRowPos == checkingMove.to_row && curColPos == checkingMove.to_col) {
                break;
            }
            blockingCheckMove.to_col = curColPos;
            blockingCheckMove.to_row = curRowPos;

            for (int row = 0; row < ROWS; row++) {
                for (int col = 0; col < COLS; col++) {
                    if (board[row][col].color == playerColor && board[row][col].type != Blank) {
                        blockingCheckMove.from_col = col;
                        blockingCheckMove.from_row = row;
                        blockingCheckMove.piece = board[row][col];
                        if (isLegal(blockingCheckMove, board, NULL, NULL)) {
                            return false;
                        }
                    }
                }
            }
            curColPos += colDirection;
            curRowPos += rowDirection;
        }
    }

    Move capturingCheckMove;
    capturingCheckMove.to_col = checkingMove.from_col;
    capturingCheckMove.to_row = checkingMove.from_row;

    for (int row = 0; row < ROWS; row++) {
        for (int col = 0; col < COLS; col++) {
            if (board[row][col].color == playerColor && board[row][col].type != Blank) {
                capturingCheckMove.from_col = col;
                capturingCheckMove.from_row = row;
                capturingCheckMove.piece = board[row][col];
                if (isLegal(capturingCheckMove, board, NULL, NULL)) {
                    return false;
                }
            }
        }
    }

    int kingMoveOffsets[8][2] = {{1, -1}, {1, 0}, {1, 1}, {0, 1}, {0, -1}, {-1, -1}, {-1, 0}, {-1, 1}};
    Move kingMove = locateKing(board, playerColor);
    kingMove.from_col = kingMove.to_col;
    kingMove.from_row = kingMove.to_row;
    kingMove.piece = board[kingMove.from_row][kingMove.from_col];
    for (int i = 0; i < 8; i++) {
        kingMove.to_col = kingMove.from_col + kingMoveOffsets[i][0];
        kingMove.to_row = kingMove.from_row + kingMoveOffsets[i][1];
        if (outOfBounds(kingMove.to_col, kingMove.to_row)) {
            continue;
        }
        if (isLegal(kingMove, board, NULL, NULL)) {
            return false;
        }
    }

    return true;
}

FILE* sopen(const char* program) {
    int fds[2];
    pid_t pid;

    if (socketpair(AF_UNIX, SOCK_STREAM, 0, fds) < 0)
        return NULL;

    switch (pid = vfork()) {
        case -1: /* Error */
            close(fds[0]);
            close(fds[1]);
            return NULL;
        case 0: /* child */
            close(fds[0]);
            dup2(fds[1], 0);
            dup2(fds[1], 1);
            close(fds[1]);
            execl("/bin/sh", "sh", "-c", program, NULL);
            _exit(127);
    }
    /* parent */
    close(fds[1]);
    return fdopen(fds[0], "r+");
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);

    setlocale(LC_CTYPE, "");

    Piece** board = (Piece**)(malloc(sizeof(Piece*) * ROWS));
    for (int i = 0; i < COLS; i++)
        board[i] = (Piece*)(malloc(sizeof(Piece) * COLS));
    initBoard(board);
    puts("Welcome to the chess GAUNTLET. I used some sortof fish to ensure you cannot beat me.");
    char stockfish_buffer[1024];
    FILE* stockfish = sopen("./stockfish");
    if (stockfish == NULL)
        printf("stockfish failed to load\n");

    fgets(stockfish_buffer, 1024, stockfish);
    fputs("uci\n", stockfish);
    while (strncmp(stockfish_buffer, "uciok", 5) != 0) {
        fgets(stockfish_buffer, 1024, stockfish);
    }
    Color current_player;
    Move aMove;
    Move* checkingMove = malloc(sizeof(Move));
    signed char wins = 0;
    bool* canCastleLeft = malloc(sizeof(bool));
    bool* canCastleRight = malloc(sizeof(bool));
    char runCommand[14];
    sprintf(runCommand, "go depth %d\n", DEPTH);
    while (wins != 100 || current_player == White) {
        *canCastleLeft = true;
        *canCastleRight = true;
        initBoard(board);
        current_player = White;

        fputs("ucinewgame\nisready\n", stockfish);

        while (strncmp(stockfish_buffer, "readyok", 7) != 0) {
            fgets(stockfish_buffer, 1024, stockfish);
        }

        printf("You currently have %d wins.\n", wins);
        while (true) {
            char* boardFen = boardToFen(board, current_player, *canCastleLeft, *canCastleRight);
            printBoard(board);
            bool beforeCastleState = *canCastleLeft || *canCastleRight;

            if (current_player == Black) {
                fprintf(stockfish, "position fen %s\n", boardFen);

                fputs("isready\n", stockfish);
                while (strncmp(stockfish_buffer, "readyok", 7) != 0) {
                    fgets(stockfish_buffer, 1024, stockfish);
                }

                fputs(runCommand, stockfish);
                while (strncmp(stockfish_buffer, "bestmove", 8) != 0) {
                    fgets(stockfish_buffer, 1024, stockfish);
                }

                char move[5];
                sscanf(stockfish_buffer, "bestmove %s ponder", move);
                printf("Stockfish played %s\n", move);
                int fromCol = move[0] - 'a';
                int toCol = move[2] - 'a';
                int fromRow = 8 - (move[1] - '0');
                int toRow = 8 - (move[3] - '0');
                Piece movingPiece = board[fromRow][fromCol];
                aMove = (Move){fromRow, fromCol, toRow, toCol, movingPiece};

            } else {
                printf("FEN: %s\n", boardFen);

                bool moveIsLegal = false;
                while (!moveIsLegal) {
                    aMove = getMove(current_player, board);

                    moveIsLegal = isLegal(aMove, board, canCastleLeft, canCastleRight);
                    if (!moveIsLegal) {
                        puts("That is not a legal chess move.");
                    }
                }
            }

            int pawnPromotionRow = (aMove.piece.color == Black) ? 7 : 0;
            if (aMove.piece.type == Pawn && aMove.to_row == pawnPromotionRow) {
                aMove.piece.type = Queen;
            }

            bool afterCastleState = *canCastleLeft || *canCastleRight;
            if (afterCastleState == false && beforeCastleState && aMove.piece.type == King && aMove.from_col == 4) {
                if (aMove.to_col == 2) {
                    board[aMove.to_row][0] = (Piece){Blank, White};
                    board[aMove.to_row][2 + 1] = (Piece){Rook, aMove.piece.color};
                } else if (aMove.to_col == COLS - 1 - 1) {
                    board[aMove.to_row][COLS - 1 - 2] = (Piece){Rook, aMove.piece.color};
                    board[aMove.to_row][COLS - 1] = (Piece){Blank, White};
                }
            }

            if (aMove.piece.type == Pawn && moveIsCapture(aMove, board) == false && aMove.to_col != aMove.from_col) {
                board[aMove.from_row][aMove.to_col] = (Piece){Blank, White};
            }

            board[aMove.to_row][aMove.to_col] = aMove.piece;
            board[aMove.from_row][aMove.from_col] = (Piece){Blank, White};

            current_player = (current_player == White) ? Black : White;

            bool isCheck = isInCheck(board, current_player, checkingMove);
            if (isCheck) {
                if (isCheckmate(*checkingMove, board)) {
                    if (current_player == White) {
                        puts("You lose :(");
                        wins--;
                    } else {
                        puts("You win :)");
                        wins++;
                    }
                    break;
                } else {
                    puts("Check!");
                }
            }
        }
    }

    if (current_player == Black) {
        FILE* flag;
        int c;
        flag = fopen("flag.txt", "r");
        if (flag) {
            while ((c = getc(flag)) != EOF) {
                putchar(c);
            }
            putchar('\n');
            fclose(flag);
        } else {
            puts("Flag is missing :/");
        }
    } else {
        puts("How is this possible?? You didn't win the 100th game!");
        puts("I won't stand a cheater!!!");
        exit(96);
    }
}