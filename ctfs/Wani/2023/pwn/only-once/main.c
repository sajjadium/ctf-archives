#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void init() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  alarm(180);
}

int rand_gen() { return rand() % 1000; }

void win() { system("/bin/sh"); }

int main() {
  init();
  srand((unsigned int)time(NULL));

  int x = rand_gen(), y = rand_gen();
  int score = 0, chall = 1;
  char buf[8];

  while (1) {
    printf("\n+---------------------------------------+\n");
    printf("| your score: %d, remaining %d challenges |\n", score, chall);
    printf("+---------------------------------------+\n\n");

    if (chall == 0) {
      printf("Bye!\n");
      break;
    }
    printf("%3d + %3d = ", x, y);
    scanf("%8s", buf);
    if (atoi(buf) == x + y) {
      printf("Cool!\n");
      score++;
    } else {
      printf("Oops...\n");
      score = 0;
    }
    if (score >= 3) {
      printf("Congrats!\n");
      win();
    }

    x = rand_gen();
    y = rand_gen();
    chall--;
  }
  return 0;
}
