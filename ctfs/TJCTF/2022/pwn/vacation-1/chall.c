#include <stdio.h>
#include <stdlib.h>

void shell_land() {
  system("/bin/sh");
}

void vacation() {
  char buf[16];
  puts("Where am I going today?");
  fgets(buf, 64, stdin);
}

void main() {
  setbuf(stdout, NULL);
  vacation();
  puts("hmm... that doesn't sound very interesting...");
}
