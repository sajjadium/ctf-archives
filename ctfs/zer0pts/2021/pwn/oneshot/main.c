#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
  int *arr = NULL, n = 0, i = 0;

  printf("n = ");
  scanf("%d", &n);
  if (n >= 0x100)
    exit(1);

  arr = calloc(n, sizeof(int));
  printf("i = ");
  scanf("%d", &i);

  printf("arr[%d] = ", i);
  scanf("%d", &arr[i]);
  puts("Done!");

  return 0;
}

__attribute__((constructor))
void setup() {
  alarm(60);
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
}
