#include <stdio.h>

int main() {
  char buf[8];
  syscall(0, 0, buf, 0x900);
}
