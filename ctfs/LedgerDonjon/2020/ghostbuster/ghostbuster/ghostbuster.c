#include <err.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <sys/prctl.h>

#include "libcheck.h"

uint8_t xor(uint8_t a, uint8_t b)
{
  return a ^ b;
}

uint8_t or(uint8_t a, uint8_t b)
{
  return a | b;
}

int main(int argc, char *argv[])
{
  pid_t pid = getpid();

  _xor = xor;
  _or = or;
  srand(pid);

  if (chdir("/home/ghostbuster") != 0) {
    err(1, "chdir");
  }

  fprintf(stderr, "[%d] please enter your secret: ", pid);
  fflush(stderr);

  uint8_t buf[SECRET_SIZE+1] = { 0 };
  if (read(STDIN_FILENO, buf, sizeof(buf)) == -1) {
    err(1, "read");
  }

  if (check_secret(buf, SECRET_SIZE) == true) {
    fprintf(stderr, "yay!\n");
  } else {
    fprintf(stderr, "nope.\n");
  }

  return 0;
}
