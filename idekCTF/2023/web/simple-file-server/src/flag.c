#include <stdio.h>
#include <stdlib.h>

char buf[100];
int main() {
  FILE *f = fopen("flag.txt", "r");
  fgets(&buf, 100, f);
  fclose(f);
  puts(buf);
}
