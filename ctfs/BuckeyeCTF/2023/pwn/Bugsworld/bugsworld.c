#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>

void win() {
  printf("WINNER!\n");
  FILE *f = fopen("flag.txt", "r");
  char flag[200];
  unsigned long length = fread(flag, 1, sizeof(flag) - 1, f);
  flag[length] = '\0';
  printf("%s\n", flag);
  exit(0);
}

enum Instruction {
  INSTRUCTION_MOVE = 0,
  INSTRUCTION_TURNLEFT = 1,
  INSTRUCTION_TURNRIGHT = 2,
  INSTRUCTION_INFECT = 3,
  INSTRUCTION_SKIP = 4,
  INSTRUCTION_HALT = 5,
  INSTRUCTION_JUMP = 6,
  INSTRUCTION_JUMP_IF_NOT_NEXT_IS_EMPTY = 7,
  INSTRUCTION_JUMP_IF_NOT_NEXT_IS_NOT_EMPTY = 8,
  INSTRUCTION_JUMP_IF_NOT_NEXT_IS_WALL = 9,
  INSTRUCTION_JUMP_IF_NOT_NEXT_IS_NOT_WALL = 10,
  INSTRUCTION_JUMP_IF_NOT_NEXT_IS_FRIEND = 11,
  INSTRUCTION_JUMP_IF_NOT_NEXT_IS_NOT_FRIEND = 12,
  INSTRUCTION_JUMP_IF_NOT_NEXT_IS_ENEMY = 13,
  INSTRUCTION_JUMP_IF_NOT_NEXT_IS_NOT_ENEMY = 14,
  INSTRUCTION_JUMP_IF_NOT_RANDOM = 15,
  INSTRUCTION_JUMP_IF_NOT_TRUE = 16,
};

const char instruction_names[][32] = {
    "MOVE",
    "TURNLEFT",
    "TURNRIGHT",
    "INFECT",
    "SKIP",
    "HALT",
    "JUMP",
    "JUMP_IF_NOT_NEXT_IS_EMPTY",
    "JUMP_IF_NOT_NEXT_IS_NOT_EMPTY",
    "JUMP_IF_NOT_NEXT_IS_WALL",
    "JUMP_IF_NOT_NEXT_IS_NOT_WALL",
    "JUMP_IF_NOT_NEXT_IS_FRIEND",
    "JUMP_IF_NOT_NEXT_IS_NOT_FRIEND",
    "JUMP_IF_NOT_NEXT_IS_ENEMY",
    "JUMP_IF_NOT_NEXT_IS_NOT_ENEMY",
    "JUMP_IF_NOT_RANDOM",
    "JUMP_IF_NOT_TRUE",
};

typedef struct State {
  uint64_t pc;
  int x;
  int y;
  int rotation;
} State;

#define BOARD_SIZE 15

#define BYTECODE_SIZE 1000
uint64_t bytecode[BYTECODE_SIZE];

void do_move(State *state) {
  switch (state->rotation) {
  case 0: // right
    state->x++;
    break;
  case 1: // up
    state->y--;
    break;
  case 2: // left
    state->x--;
    break;
  case 3: // down
    state->y++;
    break;
  }
  if (state->x < 0)
    state->x = 0;
  if (state->x >= BOARD_SIZE)
    state->x = BOARD_SIZE - 1;
  if (state->y < 0)
    state->y = 0;
  if (state->y >= BOARD_SIZE)
    state->y = BOARD_SIZE - 1;
  state->pc++;
}

void do_turnleft(State *state) {
  state->rotation++;
  if (state->rotation >= 4)
    state->rotation -= 4;
  state->pc++;
}

void do_turnright(State *state) {
  state->rotation--;
  if (state->rotation < 0)
    state->rotation += 4;
  state->pc++;
}

void do_skip(State *state) { state->pc++; }

void do_not_implemented(State *state) {
  printf("Not implemented\n");
  exit(1);
}

void do_jump(State *state) {
  state->pc++;
  state->pc = bytecode[state->pc];
}

void dont_jump(State *state) {
  state->pc++;
  state->pc++;
}

bool next_is_out_of_bounds(State *state) {
  int oldx = state->x;
  int oldy = state->y;
  int oldpc = state->pc;
  do_move(state);
  state->pc = oldpc;
  if (state->x == oldx && state->y == oldy) {
    return true;
  }
  state->x = oldx;
  state->y = oldy;
  return false;
}

void do_jump_if_not_next_is_empty(State *state) {
  if (next_is_out_of_bounds(state))
    do_jump(state);
  else
    dont_jump(state);
}

void do_jump_if_not_next_is_not_empty(State *state) {
  if (!next_is_out_of_bounds(state))
    do_jump(state);
  else
    dont_jump(state);
}

void do_jump_if_random(State *state) {
  if (rand() % 2 == 0)
    do_jump(state);
  else
    dont_jump(state);
}

typedef void (*InstructionFunction)(State *);

InstructionFunction instruction_table[] = {
    do_move,                          // MOVE
    do_turnleft,                      // TURNLEFT
    do_turnright,                     // TURNRIGHT
    do_not_implemented,               // INFECT
    do_skip,                          // SKIP
    do_not_implemented,               // HALT (it stops before running this)
    do_jump,                          // JUMP
    do_jump_if_not_next_is_empty,     // JUMP_IF_NOT_NEXT_IS_EMPTY
    do_jump_if_not_next_is_not_empty, // JUMP_IF_NOT_NEXT_IS_NOT_EMPTY
    do_jump_if_not_next_is_not_empty, // JUMP_IF_NOT_NEXT_IS_WALL
    do_jump_if_not_next_is_empty,     // JUMP_IF_NOT_NEXT_IS_NOT_WALL
    do_not_implemented,               // JUMP_IF_NOT_NEXT_IS_FRIEND
    do_not_implemented,               // JUMP_IF_NOT_NEXT_IS_NOT_FRIEND
    do_not_implemented,               // JUMP_IF_NOT_NEXT_IS_ENEMY
    do_not_implemented,               // JUMP_IF_NOT_NEXT_IS_NOT_ENEMY
    do_jump_if_random,                // JUMP_IF_NOT_RANDOM
    dont_jump,                        // JUMP_IF_NOT_TRUE
};

void print_state(State *state) {
  for (int y = 0; y < BOARD_SIZE; y++) {
    for (int x = 0; x < BOARD_SIZE; x++) {
      if (x == state->x && y == state->y) {
        switch (state->rotation) {
        case 0:
          putc('>', stdout);
          break;
        case 1:
          putc('^', stdout);
          break;
        case 2:
          putc('<', stdout);
          break;
        case 3:
          putc('v', stdout);
          break;
        }
      } else {
        putc('.', stdout);
      }
    }
    putc('\n', stdout);
  }
}

void run_program() {
  printf("How many instructions in your bytecode?\n> ");
  uint32_t n;
  scanf("%u", &n);
  n += 1; // room for final HALT instruction
  if (n >= BYTECODE_SIZE) {
    printf("That's too many\n");
    exit(1);
  }
  printf("Enter your instructions:\n> ");
  for (uint32_t i = 0; i < n - 1; i++) {
    scanf("%lu", &bytecode[i]);
  }
  bytecode[n - 1] = INSTRUCTION_HALT;

  // show the disassembly and validate program
  for (int i = 0; i < n; i++) {
    printf("%s", instruction_names[bytecode[i]]);
    if (bytecode[i] < 0 || bytecode[i] > 16) {
      printf("Invalid instruction\n");
      return;
    }
    if (bytecode[i] >= INSTRUCTION_JUMP) {
      i++;
      printf(" %ld\n", bytecode[i]);
    } else {
      printf("\n");
    }
  }

  // run the program
  State state = {0};

  print_state(&state);
  usleep(25000);
  printf("\n\n");
  while (bytecode[state.pc] != INSTRUCTION_HALT) {
    instruction_table[bytecode[state.pc]](&state);
    print_state(&state);
    usleep(25000);
    printf("\n\n");
  }
}

int main() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);

  printf("Welcome to BUGSWORLD!\n");
  while (1) {
    run_program();
  }
}