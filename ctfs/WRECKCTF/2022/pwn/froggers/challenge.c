// compiled with gcc -fno-stack-protector -o challenge challenge.c

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <stdbool.h>

bool frog = false;
bool coin = false;
bool wallet_supports_frog_coin = false;

void lilypad(char *buffer) {
  fgets(buffer, 40, stdin);
}

void set_frog() {
  puts("Setting frog...");
  frog = wallet_supports_frog_coin;
  if (frog)
    puts("Frog set!");
  fflush(stdout);
}

void set_coin() {
  puts("Setting coin...");
  coin = frog;
  if (coin)
    puts("Coin set!");
  fflush(stdout);
}

void froggers(char *name) {
  printf("Hi %s", name);

  if (frog && coin) {
    FILE *fp = fopen("flag.txt", "r");
    if (fp == NULL)
      return;

    fseek(fp, 0, SEEK_END);
    long fsize = ftell(fp);
    fseek(fp, 0, SEEK_SET);

    char flag[fsize + 1];
    flag[fsize] = 0;

    fread(flag, 1, fsize, fp);

    if (!frog || !coin) {
      puts("Frogger error!");
      fflush(stdout);
      exit(1);
    }

    printf("%s\n", flag);

    fclose(fp);
  } else {
    puts("Your wallet doesn't have frog coins!");
  }
  fflush(stdout);
}

int main() {
  printf("Hey I'm %p, what's your name?\n", main);
  fflush(stdout);

  char name[16];
  lilypad(name);

  froggers(name);

  if (!wallet_supports_frog_coin) {
    wallet_supports_frog_coin = true;
  }

  return 0;
}
