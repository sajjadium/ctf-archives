#include "util.h"

void __attribute__((noreturn)) printError(char *msg) {
  puts(msg);
  _exit(0);
}

