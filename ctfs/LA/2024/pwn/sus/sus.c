#include <stdio.h>

void sus(long s) {}

int main(void) {
  setbuf(stdout, NULL);
  long u = 69;
  puts("sus?");
  char buf[42];
  gets(buf);
  sus(u);
}
