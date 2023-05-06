#include <stdio.h>
#include <stdlib.h>

void init() {
  // alarm(600);
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
}

void win() { system("/bin/sh"); }

int main() {
  char nope[20];
  init();
  while (strcmp(nope, "YES")) {
    printf("You can't overwrite return address if canary is enabled.\nDo you "
           "agree with me? : ");
    scanf("%s", nope);
    printf(nope);
  }
}