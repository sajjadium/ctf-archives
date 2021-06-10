#include <stdio.h>
#include <unistd.h>
#include "utils.h"
#include "auth.h"

int babyauth(const char *dir) {
  /* Auth 1: Username */
  if (authenticator(dir, username_validator, username_reader) != 0)
    fatal("Authentication failed");

  /* Auth 2: Password */
  if (authenticator(dir, password_validator, password_reader) != 0)
    fatal("Authentication failed");

  /* Auth 3: One time token */
  if (authenticator(dir, token_validator, token_reader) != 0)
    fatal("Authentication failed");

  return 0;
}

int main(int argc, char **argv) {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  alarm(180);

  if (argc < 2) {
    printf("Usage: %s <WORKDIR>\n", argv[0]);
    return 1;
  }

  /* BABYAUTH! */
  return babyauth(argv[1]);
}
