#include <stdio.h>

int main() {
  char name[0x100];
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  puts("Enter something");
  scanf("%s", name);
  return 0;
}
