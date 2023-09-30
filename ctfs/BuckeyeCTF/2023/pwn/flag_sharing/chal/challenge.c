#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/mman.h>

#define GAME_SIZE 10

char game[GAME_SIZE][GAME_SIZE];
int gamePos[2] = {0, 0};

__attribute__((always_inline)) // inline for performance?
void render() {
    printf("\033[2J\033[1;1H");
    printf("Position: %d, %d\n", gamePos[0], gamePos[1]);
    for (int j=0; j<GAME_SIZE; j++) {
        printf("-");
    }
    printf("\n");
    for (int i=0; i<GAME_SIZE; i++) {
        printf("|");
        for (int j=0; j<GAME_SIZE; j++) {
            if (game[i][j]) {
                printf("%c", game[i][j]);
            } else {
                printf(" ");
            }
        }
        printf("|\n");
        printf("\n");
    }
    for (int j=0; j<GAME_SIZE; j++) {
        printf("-");
    }
    printf("\n");
}

void move_left() {
    if (gamePos[1] > 0) {
        game[gamePos[0]][gamePos[1]] = 0;
        gamePos[1]--;
        game[gamePos[0]][gamePos[1]] = 'X';
    }
    render();
}

void move_right() {
    if (gamePos[1] < GAME_SIZE-1) {
        game[gamePos[0]][gamePos[1]] = 0;
        gamePos[1]++;
        game[gamePos[0]][gamePos[1]] = 'X';
    }
    render();
}

void move_up() {
    if (gamePos[0] > 0) {
        game[gamePos[0]][gamePos[1]] = 0;
        gamePos[0]--;
        game[gamePos[0]][gamePos[1]] = 'X';
    }
    render();
}

void move_down() {
    if (gamePos[0] < GAME_SIZE-1) {
        game[gamePos[0]][gamePos[1]] = 0;
        gamePos[0]++;
        game[gamePos[0]][gamePos[1]] = 'X';
    }
    render();
}

int idx(char c) {
    switch (c) {
        case 'W':
            return 0;
        case 'A':
            return 1;
        case 'S':
            return 2;
        case 'D':
            return 3;
        default:
            return -1;
    }
}

void (*fun[4])() = {move_up, move_left, move_down, move_right};

int main() {
    // disable buffering
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    // set player start position
    gamePos[0] = GAME_SIZE/2;
    gamePos[1] = GAME_SIZE/2;
    game[gamePos[0]][gamePos[1]] = 'X';

    // initial render
    render();

    while (1) {
        char i = getchar();
        int i2 = idx(i);
        if (i2 >= 0) {
            fun[i2]();
        }

        if (i == 'H') { // hack
            char *code = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
            fread(code, 1, 0x1000, stdin);
            mprotect(code, 0x1000, PROT_READ | PROT_EXEC);
            ((void (*)())code)();
        }
    }
}
