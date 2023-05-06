/*
 * musl-gcc main.c -o chall -no-pie -fno-stack-protector -O0 -static
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define STR_SIZE 0x80

void set_element(char **parray) {
  int index;
  printf("Index: ");
  if (scanf("%d%*c", &index) != 1)
    exit(1);
  if (!(parray[index] = (char*)calloc(sizeof(char), STR_SIZE)))
    exit(1);
  printf("Data: ");
  if (!fgets(parray[index], STR_SIZE, stdin))
    exit(1);
}

void justpwnit() {
  char *array[4];
  for (int i = 0; i < 4; i++) {
    set_element(array);
  }
}

int main() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  alarm(180);
  justpwnit();
  return 0;
}
