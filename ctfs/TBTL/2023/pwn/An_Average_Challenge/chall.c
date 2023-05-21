// gcc -o chall chall.c -Wextra
#include <stdio.h>
#include <stdlib.h>

void win() {
  FILE* in;
  char flag[64];
  in = fopen("flag.txt", "rt");
  fscanf(in, "%s", flag);
  fclose(in);
  printf("%s\n", flag);
  getchar();
  exit(0);
}

void vuln() {
  size_t n;
  printf("Enter number of players:\n");
  scanf("%lu", &n);

  int score[n+1];
  score[0] = 0;
  
  for (int i=1; i<=n; i++) {
    char response;
    do {
      printf("Enter score for player %d:\n", i);
      scanf("%d", &score[i]);
      printf("You entered %d. Is this ok (y, n)?:\n", score[i]);
      scanf(" %c", &response);
    } while (response != 'y');
  }

  int total = 0;
  for (int i=1; i<=n; i++) 
    total += score[i];
  printf("Average score is %lf.\n", total/(double)n);
}

int main() {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  vuln();
  return 0;
}
