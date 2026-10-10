// gcc -o chall chall.c

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char flag[64];
int flag_length;

void read_flag() {
  FILE* in;
  
  in = fopen("flag.txt", "rt");
  fgets(flag, 64, in);
  flag_length = strlen(flag);
  fclose(in);
}

void guess_flag() {
  int guess_length;
  char *guess;
  int ncorrect;
  int i;
  
  puts("Try to guess the flag!");
  puts("Enter the length of your guess:");
  scanf("%d", &guess_length);
  getchar();
  guess = malloc(guess_length);
  puts("Enter your guess:");
  fgets(guess, guess_length, stdin);

  ncorrect = 0;
  for (i=0; i<guess_length && i<flag_length; i++)
    if (guess[i] == flag[i])
      ncorrect++;

  if (ncorrect == flag_length)
    puts("Got it!");
  else if (ncorrect == flag_length-2)
    puts("Almost!");
  else if (ncorrect*2 >= flag_length)
    puts("Getting there!");
  else
    puts("Not even close.");
  
  free(guess);
}

int main() {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  read_flag();
  guess_flag();
  return 0;
}
