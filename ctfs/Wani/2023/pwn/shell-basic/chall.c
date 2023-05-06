#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
  char code[1024];
  printf("Enter shellcode: ");
  fgets(code, sizeof(code), stdin);
  void (*shellcode)() = (void (*)())code;
  shellcode();
  return 0;
}
