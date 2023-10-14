#include "util.h"

void __attribute__((noreturn)) error(char *msg) {
  puts(msg);
  _exit(0);
}


