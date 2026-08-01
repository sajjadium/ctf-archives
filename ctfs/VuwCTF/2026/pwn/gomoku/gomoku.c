// gomoku.c : text-based 16x16 Gomoku (five-in-a-row) board game.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define N 16                 // 16x16 board, 256 cells, 256-bit bitboard

enum { BLACK = 0, WHITE = 1 };

typedef struct {
    uint64_t cells[4];       // 256 bits; cells[0] = bits 0..63, ... cells[3] = bits 192..255
} Bitboard;

typedef struct {
    Bitboard side[2];        // side[BLACK], side[WHITE]
    int      turn;           // whose move it is
    int      moves;          // ply count
    char     p1[16];         // player names
    char     p2[16];
} Game;

// 256-bit logical right shift (cells[0] is the low word), 0 <= n < 256.
static void rshift256(Bitboard *out, const Bitboard *in, unsigned n) {
    unsigned word = n >> 6;
    unsigned bit  = n & 63;
    for (int i = 0; i < 4; i++) out->cells[i] = 0;
    for (int i = 0; i < 4; i++) {
        if (i + word < 4)
            out->cells[i] |= in->cells[i + word] >> bit;
        if (bit && i + word + 1 < 4)
            out->cells[i] |= in->cells[i + word + 1] << (64 - bit);
    }
}

// Five-in-a-row detection using stride bitshifts, and masks
// to exclude wins detected across boundaries.
static int has_five(const Bitboard *b) {
    static const struct { unsigned s; uint64_t mask; } dirs[4] = {
        {  1, 0x0FFF0FFF0FFF0FFFULL },  // horizontal        : anchor col 0..11
        { 16, 0xFFFFFFFFFFFFFFFFULL },  // vertical          : no mask needed
        { 17, 0x0FFF0FFF0FFF0FFFULL },  // diagonal  (r+1,c+1): anchor col 0..11
        { 15, 0xFFF0FFF0FFF0FFF0ULL },  // anti-diag (r+1,c-1): anchor col 4..15
    };
    for (int d = 0; d < 4; d++) {
        Bitboard acc;
        for (int i = 0; i < 4; i++) acc.cells[i] = b->cells[i];
        for (int k = 1; k < 5; k++) {
            Bitboard sh;
            rshift256(&sh, b, dirs[d].s * k);
            for (int i = 0; i < 4; i++) acc.cells[i] &= sh.cells[i];
        }
        for (int i = 0; i < 4; i++) acc.cells[i] &= dirs[d].mask;
        if (acc.cells[0] | acc.cells[1] | acc.cells[2] | acc.cells[3]) return 1;
    }
    return 0;
}

static int cell_set(const Bitboard *bb, long idx) {
    return (int)((bb->cells[idx >> 6] >> (idx & 63)) & 1ULL);
}

static void print_board(FILE *out, const Game *g) {
    fprintf(out, "\n     ");
    for (int c = 0; c < N; c++) fprintf(out, "%x ", c);
    fprintf(out, "\n");
    for (int r = 0; r < N; r++) {
        fprintf(out, "  %x  ", r);
        for (int c = 0; c < N; c++) {
            long idx = (long)r * N + c;
            char ch = '.';
            if (cell_set(&g->side[BLACK], idx)) ch = 'X';
            else if (cell_set(&g->side[WHITE], idx)) ch = 'O';
            fprintf(out, "%c ", ch);
        }
        fprintf(out, "\n");
    }
    fprintf(out, "\n");
}

static void read_line(char *buf, size_t n) {
    if (!fgets(buf, (int)n, stdin)) exit(0);
    buf[strcspn(buf, "\n")] = '\0';
}

static void read_names(Game *g) {
    printf("Black player, enter your name: ");
    read_line(g->p1, sizeof g->p1);
    printf("White player, enter your name: ");
    read_line(g->p2, sizeof g->p2);
}

static void run_game(Game *g) {
    FILE *out = stdout;

    for (;;) {
        print_board(out, g);
        fprintf(out, "%s to move (%c).\n",
                g->turn == BLACK ? g->p1 : g->p2,
                g->turn == BLACK ? 'X' : 'O');
        fprintf(out,
                "  1) place stone\n"
                "  2) remove stone\n"
                "  3) peek cell\n"
                "  4) resign\n"
                "> ");

        int choice;
        if (scanf("%d", &choice) != 1) return;
        if (choice == 4) {
            fprintf(out, "%s resigns. Goodbye.\n",
                    g->turn == BLACK ? g->p1 : g->p2);
            return;
        }

        fprintf(out, "row col: ");
        int row, col;
        if (scanf("%d %d", &row, &col) != 2) {
            int c;
            while ((c = getchar()) != '\n' && c != EOF) { }
            continue;
        }

        if (row > 15 || col > 15) {
            fprintf(out, "that square is off the board\n");
            continue;
        }

        long      idx  = (long)row * N + col;
        Bitboard *bb   = &g->side[g->turn];
        long      limb = idx >> 6;
        unsigned  bit  = (unsigned)(idx & 63);

        switch (choice) {
        case 1:  // place
            bb->cells[limb] |= (1ULL << bit);
            g->moves++;
            if (has_five(bb)) {
                print_board(out, g);
                fprintf(out, "Five in a row! %s wins!\n",
                        g->turn == BLACK ? g->p1 : g->p2);
                return;
            }
            g->turn ^= 1;
            break;
        case 2:  // remove
            bb->cells[limb] &= ~(1ULL << bit);
            break;
        case 3:  // peek
            fprintf(out, "cell (%d,%d) = %d\n", row, col,
                    (int)((bb->cells[limb] >> bit) & 1ULL));
            break;
        default:
            fprintf(out, "unknown option\n");
            break;
        }
    }
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin,  NULL, _IONBF, 0);

    Game g;
    memset(&g, 0, sizeof g);

    puts("=== GOMOKU :: five in a row ===");
    read_names(&g);
    run_game(&g);
    return 0;
}
