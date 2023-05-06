/* gcc -o more-printf -fstack-protector-all more-printf.c */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

FILE *fp;
char *buffer;
uint64_t i = 0x8d9e7e558877;

_Noreturn main() {
  /* Just to save some of your time */
  uint64_t *p;
  p = &p;

  /* Chall */
  setbuf(stdin, 0);
  buffer = (char *)malloc(0x20 + 1);
  fp = fopen("/dev/null", "wb");
  fgets(buffer, 0x1f, stdin);
  if (i != 0x8d9e7e558877) {
    _exit(1337);
  } else {
    i = 1337;
    fprintf(fp, buffer);
    _exit(1);
  }
}
