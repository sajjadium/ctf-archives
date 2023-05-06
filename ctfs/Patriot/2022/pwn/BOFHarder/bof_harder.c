#include<stdio.h>
#include<stdlib.h>

// gcc -fno-stack-protector -z execstack -o bof_harder bof_harder.c

int main() {
  char stack = 0;
  char buf[128] = {0};

  printf("This buffer overflow should be a little bit more difficult than the begginer buffer overflow.\n");
  printf("%p\n", &stack);

  fgets(buf, 10000, stdin);

  return 0;
}