#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

static void random_open() {
  int r = open("/dev/random", O_RDONLY);
  if (r < 0) exit(1);
  int n = 0;
  read(r, &n, 2);
  n &= 511;
  for (int i = 0; i < n; i++)
    open("/dev/random", O_RDONLY);
}

int main() {
  char buf[30];
  setbuf(stdout, NULL);
  printf("stack address @ %p\n", buf);
  read(0, buf, 300);
  fclose(stdin);
  fclose(stdout);
  fclose(stderr);
  random_open();
  return 0;
}
