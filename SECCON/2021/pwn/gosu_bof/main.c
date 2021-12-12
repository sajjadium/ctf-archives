#include <stdio.h>

int main(void) {
  char buf[0x80];
  gets(buf);
  return 0;
}
