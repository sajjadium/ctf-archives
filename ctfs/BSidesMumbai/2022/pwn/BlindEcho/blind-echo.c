#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char buf[128] = {0};

int search(char *buf, char c) {
  for(int i = 0; buf[i] != '\0'; i++) {
    if(buf[i] == c) return 1;
  }
  return 0;
}

int main() {
  char *ptr = buf;

  sleep(2);
  setbuf(stdout, NULL);
  alarm(0x8);

  printf("0x%lx 0x%lx\n", (unsigned long)(&ptr) & 0xffff, (unsigned long)(&main) & 0xffff);
  fgets(buf, sizeof(buf), stdin);
  if(search(buf, '*')) exit(-1);

  if(!freopen("/dev/null", "w", stderr)) exit(-1);
  fprintf(stderr, buf);

  printf("bye\n");
  return 0;
}
