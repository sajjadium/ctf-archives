#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
  char size[16], fmt[8], *buf;

  printf("size: ");
  scanf("%15s", size);
  if (!isdigit(*size)) {
    puts("[-] Invalid number");
    exit(1);
  }

  buf = (char*)malloc(atoi(size) + 1);

  printf("data: ");
  snprintf(fmt, sizeof(fmt), "%%%ss", size);
  scanf(fmt, buf);

  exit(0);
}

__attribute__((constructor))
void setup(void) {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
  alarm(180);
}
