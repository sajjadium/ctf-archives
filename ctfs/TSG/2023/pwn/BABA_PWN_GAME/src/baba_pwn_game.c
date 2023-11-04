#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <stdlib.h>

#define FLAG_STAGE_NAME "hard.y"
#define STAGE_W 32
#define STAGE_H 16
#define CHR_NUM 16
#define HISTORY_MAX 1000

const char *object_chars = "SI@O#6!WNX<>v^*H";

struct GameState {
  // meta values
  char stage_name[64];
  unsigned short spawn_off;
  char history[HISTORY_MAX + 64];
  // stage data
  unsigned short stage[STAGE_H][STAGE_W];
  unsigned short is_push[CHR_NUM]; // you can push this object if you move into a cell with the object
  unsigned short is_stop[CHR_NUM]; // you cannot move into a cell with this object
  unsigned short is_you[CHR_NUM];  // you can controll this object with WASD keys
  unsigned short is_sink[CHR_NUM]; // all objects in a cell are destroyed when something come onto a cell with the object
  unsigned short is_open[CHR_NUM]; // when *open* and *shut* objects are in the same cell, both are destroyed
  unsigned short is_shut[CHR_NUM]; // when *open* and *shut* objects are in the same cell, both are destroyed
  unsigned short is_win[CHR_NUM];  // you will win if *you* enter a cell with the object
  unsigned char should_update[STAGE_H][STAGE_W];
} state;

int get_object_id(char obj) {
  return strchr(object_chars, obj) - object_chars;
}

void win(void) {
  char *flag = getenv("FLAG");
  if (strcmp(state.stage_name, FLAG_STAGE_NAME) || flag == NULL) {
    printf("YOU WIN\n");
  } else {
    printf("YOU WIN FLAG: %s\n", flag);
  }
  exit(0);
}

void lose(void) {
  printf("YOU LOSE\n");
  exit(0);
}

void print_stage() {
  printf("HISTORY: %s\n", state.history);
  for (int i = 0; i < STAGE_H; i++) {
    for (int j = 0; j < STAGE_W; j++) {
      if (state.stage[i][j] == 0) {
        putc(' ', stdout);
      } else {
        putc(object_chars[__builtin_ctz(state.stage[i][j])], stdout);
      }
    }
    putc('\n', stdout);
  }
}

unsigned short to_bitset(unsigned short *rule_array) {
  unsigned short set = 0;
  for (int i = 0; i < CHR_NUM; i++) {
    if (rule_array[i]) set |= 1u << i;
  }
  return set;
}

void move(unsigned short *from, unsigned short *to, unsigned short set) {
  if (set == 0) return;
  *from &= ~set;
  if (*to & to_bitset(state.is_sink)) {
    *to = 0;
  } else {
    *to |= set;
  }
  unsigned short opens = *to & to_bitset(state.is_open);
  unsigned short shuts = *to & to_bitset(state.is_shut);
  if (opens && shuts)  *to &= ~opens & ~shuts;
}

void step_game(int dx, int dy) {
  int will_lose = 1;
  memset(state.should_update, 1, sizeof(state.should_update));

  for (int y = 0; y < STAGE_H; y++) {
    for (int x = 0; x < STAGE_W; x++) {
      unsigned short you = state.stage[y][x] & to_bitset(state.is_you);
      if (you == 0 || !state.should_update[y][x]) continue;
      will_lose = 0;

      int nx = x + dx, ny = y + dy; // next position
      if (state.stage[ny][nx] & to_bitset(state.is_stop)) continue;
      if (state.stage[ny][nx] & to_bitset(state.is_win)) win();

      int nnx = x + 2 * dx, nny = y + 2 * dy;
      unsigned short push = state.stage[ny][nx] & to_bitset(state.is_push);
      move(&state.stage[ny][nx], &state.stage[nny][nnx], push);
      move(&state.stage[y][x], &state.stage[ny][nx], you);
      state.should_update[ny][nx] = 0;
    }
  }
  if (will_lose) lose();

  // cool anti-cheat system
  for (int y = 0; y < STAGE_H; y++) {
    for (int x = 0; x < STAGE_W; x++) {
      if (state.stage[y][x] & to_bitset(state.is_you) && state.stage[y][x] & to_bitset(state.is_stop)) lose();
    }
  }
}

int main(void) {
  // *** Step 1. Initialize the game ***
  memset(&state, 0, sizeof(struct GameState));
  state.spawn_off = (STAGE_H + 1) * STAGE_W / 2;
  setbuf(stdout, NULL);

  // *** Step 2. Load the stage ***
  printf("DIFFICULTY? (easy/hard)\n");
  int i;
  for (i = 0; i < 63; i++) {
    char c = fgetc(stdin);
    if (c == '\n') break;
    if (c == '/' || c == '~') return 1; // no path traversal
    state.stage_name[i] = c;
  }
  strcpy(&state.stage_name[i], ".y");

  FILE *fp = fopen(state.stage_name, "r");
  if (fp == NULL) {
    printf("STAGE IS NOT EXIST: %s\n", state.stage_name);
    return 1;
  }
  fread(state.stage, sizeof(state.stage), 1, fp);

  // *** Step 3. Set up the rules ***
  state.is_stop[get_object_id('#')] = 1;
  state.is_win[get_object_id('6')] = 1;
  state.is_push[get_object_id('O')] = 1;
  state.is_push[get_object_id('*')] = 1;
  state.is_open[get_object_id('*')] = 1;
  state.is_shut[get_object_id('H')] = 1;
  state.is_sink[get_object_id('X')] = 1;
  state.is_you[get_object_id('@')] = 1;
  state.stage[0][state.spawn_off] |= 1 << get_object_id('@');

  // *** Step 4. Main loop ***
  for (int num_moves = 0; num_moves < HISTORY_MAX;) {
    print_stage();
    printf("> ");

    char input[32];
    if (fgets(input, 32, stdin) == NULL) break;
    for (char *c = input; *c != '\0' && num_moves < HISTORY_MAX; c++) {
      int dx = 0, dy = 0;
      if (*c == 'w') dy = -1;
      if (*c == 'a') dx = -1;
      if (*c == 's') dy = 1;
      if (*c == 'd') dx = 1;
      if (dx == 0 && dy == 0) continue;
      state.history[num_moves++] = *c;
      step_game(dx, dy);
    }
  }
  return 0;
}
