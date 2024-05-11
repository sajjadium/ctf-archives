// gcc -o chall chall.c -Wextra
#include <stdio.h>
#include <stdlib.h>

void read_flag() {
  FILE* in;
  char flag[64];
  in = fopen("flag.txt", "rt");
  fscanf(in, "%s", flag);
  fclose(in);
}

void vuln() {
  int score[20];
  int total = 0;  
  for (int i=0; i<20; i++) {
    printf("Enter score for player %d:\n", i);
    scanf("%d", &score[i]);
    total += score[i];
  }
  printf("Average score is %lf.\n", total/20.);
  printf("Type q to quit.");
  while (getchar() != 'q');
}

int main() {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  read_flag();
  vuln();
  return 0;
}
