#include <stdlib.h>
#include <stdio.h>
#include <string.h>

enum {
    TURN_COMPUTER = 0,
    TURN_PLAYER = 1
};

int playing = 0;
int turn = 0;
int player_symbol, computer_symbol;
int values[9];

void new_game() {
    memset(values, 0, sizeof(values));
    turn = rand() % 2;
    player_symbol = turn == TURN_PLAYER ? 'O' : 'X';
    computer_symbol = turn == TURN_COMPUTER ? 'O' : 'X';
    playing = 1;
}

static void check_win() {
    int winning_symbol = 0;
    for (int i = 0; i < 3; i++) {
        if (values[3 * i] != 0 && values[3 * i] == values[3 * i + 1] && values[3 * i] == values[3 * i + 2])
            winning_symbol = values[3 * i];
        if (values[i] != 0 && values[i] == values[3 + i] && values[i] == values[6 + i])
            winning_symbol = values[i];
    }
    if (values[0] != 0 && values[0] == values[3 + 1] && values[0] == values[6 + 2])
        winning_symbol = values[0];
    if (values[2] != 0 && values[2] == values[3 + 1] && values[2] == values[6])
        winning_symbol = values[2];

    if (winning_symbol != 0)
        playing = 0;
}

void player_turn(unsigned int x, unsigned int y) {
    if (!playing || turn != TURN_PLAYER || x >= 3 || y >= 3)
        return;
    if (values[3 * y + x] == 0) {
        values[3 * y + x] = player_symbol;
        turn = TURN_COMPUTER;
    }
    check_win();
}

void computer_turn() {
    if (!playing || turn != TURN_COMPUTER)
        return;
    int count = 0;
    for (int i = 0; i < 9; i++)
        if (values[i] == 0)
            count++;
    if (count == 0)
        return;
    int idx = rand() % count;
    printf("%d\n", idx);
    for (int i = 0; i < 9; i++) {
        if (values[i] != 0)
            continue;
        if (idx-- == 0) {
            values[i] = computer_symbol;
            turn = TURN_PLAYER;
            break;
        }
    }
    check_win();
}

void print() {
    puts("---");
    for (int y = 0; y < 3; y++) {
        for (int x = 0; x < 3; x++) {
            putchar(values[y * 3 + x] ? values[y * 3 + x] : ' ');
        }
        putchar('\n');
    }
    puts("---");
}
