#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define DECK_SIZE 0x52
#define QUEEN 1111111111

void setup() {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);

  srand(time(NULL));
}

void win() {
  char flag[256];

  FILE *flagfile = fopen("flag.txt", "r");

  if (flagfile == NULL) {
    puts("Cannot read flag.txt.");
  } else {
    fgets(flag, 256, flagfile);
    flag[strcspn(flag, "\n")] = '\0';
    puts(flag);
  }
}

long lrand() {
  long higher, lower;
  higher = (((long)rand()) << 32);
  lower = (long)rand();
  return higher + lower;
}

void game() {
  int index;
  long leak;
  long cards[52] = {0};
  char name[20];

  for (int i = 0; i < 52; ++i) {
    cards[i] = lrand();
  }

  index = rand() % 52;
  cards[index] = QUEEN;

  printf("==============================\n");

  printf("index of your first peek? ");
  scanf("%d", &index);
  leak = cards[index % DECK_SIZE];
  cards[index % DECK_SIZE] = cards[0];
  cards[0] = leak;
  printf("Peek 1: %lu\n", cards[0]);

  printf("==============================\n");

  printf("index of your second peek? ");
  scanf("%d", &index);
  leak = cards[index % DECK_SIZE];
  cards[index % DECK_SIZE] = cards[0];
  cards[0] = leak;
  printf("Peek 2: %lu\n", cards[0]);

  printf("==============================\n");

  printf("Show me the lady! ");
  scanf("%d", &index);

  printf("==============================\n");

  if (cards[index] == QUEEN) {
    printf("You win!\n");
  } else {
    printf("Just missed. Try again.\n");
  }

  printf("==============================\n");

  printf("Add your name to the leaderboard.\n");
  getchar();
  printf("Name: ");
  fgets(name, 52, stdin);

  printf("==============================\n");

  printf("Thanks for playing, %s!\n", name);
}

int main() {
  setup();
  printf("Welcome to 52-card monty!\n");
  printf("The rules of the game are simple. You are trying to guess which card "
         "is correct. You get two peeks. Show me the lady!\n");
  game();
  return 0;
}
