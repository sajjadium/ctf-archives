#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Field {
    char grid[3][3];
    int moves_left;
} field;

#define BLOCK "█"
#define GREEN "\e[32m"
#define RED "\e[31m"
#define RESET "\e[0m"
#define CLEAR "\e[H\e[2J\e[H"
#define COMPUTER 1
#define PLAYER 2
#define OTHER(x) (x ^ 3)
#define max(a, b) (((a) > (b)) ? (a) : (b))

void print() {
    printf(CLEAR);
    printf("       0        1        2\n\n");
    for (int i = 0; i < 3; i++) {
        if (i) printf("   --------+--------+--------\n");
        for (int _x = 0; _x < 4; _x++) {
            if (_x == 2) printf("%d  ", i);
            else printf("   ");
            for (int j = 0; j < 3; j++) {
                if (j) printf("|");
                for (int _y = 0; _y < 8; _y++) {
                    if (field.grid[j][i] == COMPUTER) printf(RED);
                    else if (field.grid[j][i] == PLAYER) printf(GREEN);
                    printf(BLOCK RESET);
                }
            }
            printf("\n");
        }
    }
}

int is_(int x, int y, int player) {
    if (x < 0 || x >= 3 || y < 0 || y >= 3) return 0;
    return field.grid[x][y] == player;
}

int is_winning_line(int x, int y, int dx, int dy, int player) {
    return (is_(x + dx, y+dy, player) + is_(x + 2*dx, y + 2*dy, player) + is_(x - dx, y - dy, player) + is_(x - 2*dx, y - 2*dy, player)) >= 2;
}

// Nevermind the duplicate work here :)
int determine_winner() {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            int p = field.grid[i][j];
            if (!p) continue;
            if (   is_winning_line(i, j, 0, 1, p)
                || is_winning_line(i, j, 1, 0, p)
                || is_winning_line(i, j, 1, 1, p)
                || is_winning_line(i, j, 1, -1, p))
                return p;
        }
    }
    return 0;
}

int score(int player) {
    int winner = determine_winner();
    if (winner == player) return 1;
    else if (winner == OTHER(player)) return -1;
    return 0;
}

int score_rec(int depth, int player) {
    int s = score(player);
    if (depth <= 0 || s != 0) return s;
    int best = -1;
    for (int c = 0; c < 3; c++) {
        for (int r = 0; r < 3; r++) {
            if (field.grid[c][r]) continue;
            field.grid[c][r] = player;
            best = max(best, -score_rec(depth - 1, OTHER(player)));
            field.grid[c][r] = 0;
        }
    }
    return best;
}

int readint() {
    while (1) {
        printf("> ");
        unsigned long len = 0;
        char* line = NULL;
        getline(&line, &len, stdin);
        if (strchr(line, '-')) {
            free(line);
            continue;
        }
        int res = atoi(line);
        if (res < 3) {
            free(line);
            return res;
        }
        free(line);
    }
}

int player_move() {
    int r, c;
    while (1) {
        printf("Row");
        r = readint();
        printf("Col");
        c = readint();
        if (!field.grid[c][r]) break;
    }
    field.moves_left--;
    field.grid[c][r] = PLAYER;
    return (   is_winning_line(c, r, 0, 1, PLAYER)
            || is_winning_line(c, r, 1, 0, PLAYER)
            || is_winning_line(c, r, 1, 1, PLAYER)
            || is_winning_line(c, r, 1, -1, PLAYER));
}

void computer_move() {
    int bestc = 0, bestr = 0;
    int m = -2;
    for (int c = 0; c < 3; c++) {
        for (int r = 0; r < 3; r++) {
            if (field.grid[c][r]) continue; // Can't play here
            field.grid[c][r] = COMPUTER;
            int s = -score_rec(field.moves_left - 1, PLAYER);
            if (s > m) {
                bestr = r;
                bestc = c;
                m = s;
            }
            field.grid[c][r] = 0;
        }
    }
    if (m == -2) abort();
    field.grid[bestc][bestr] = COMPUTER;
    field.moves_left--;
}

void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    field.moves_left = 8;
    memset(field.grid, 0, sizeof(field.grid));

    puts("Welcome. I'm certain you can't win, so I'll even let you start.");
}

void flag() {
    FILE* f = fopen("flag.txt", "r");
    char buf[100];
    fread(buf, 1, sizeof(buf) - 1, f);
    puts(buf);
}

int main() {
    init();
    print();
    for (int i = 0; i < 4; i++) {
        if (player_move()) {
            print();
            flag();
            return 0;
        }
        computer_move();
        print();
        if (determine_winner() == COMPUTER) {
            puts("I told you I'd win, didn't I?");
            return 0;
        }
    }
    puts("Playing a tie is still not winning :P");
}
