#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUF_SIZE 32
#define MAX_READ_LEN 48

void init() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  alarm(180);
}

void show_stack(char *buf) {
  printf("\n  #############################################\n");
  printf("  #                stack state                #\n");
  printf("  #############################################\n\n");

  printf("                 hex           string\n");
  for (int i = 0; i < MAX_READ_LEN; i += 8) {
    printf("       +--------------------+----------+\n");
    printf(" +0x%02x | 0x%016lx | ", i, *(unsigned long *)(buf + i));
    for (int j = 7; j > -1; j--) {
      char c = *(char *)(buf + i + j);
      if (c > 0x7e || c < 0x20)
        c = '.';
      printf("%c", c);
    }
    if (i == 40)
      printf(" | <- TARGET!!!\n");
    else
      printf(" |\n");
  }
  printf("       +--------------------+----------+\n");
}

void win() {
  asm("xor %rax, %rax\n"
      "xor %rsi, %rsi\n"
      "xor %rdx, %rdx\n"
      "mov $0x3b, %al\n"
      "mov $0x68732f6e69622f, %rdi\n"
      "push %rdi\n"
      "mov %rsp, %rdi\n"
      "syscall");
}

int ofs = 0, ret = 0;

int main() {
  init();

  char buf[BUF_SIZE] = {0};

  printf("Let's overwrite the target address with that of the win function!\n");

  while (ofs < MAX_READ_LEN) {
    show_stack(buf);

    printf("your input (max. %d bytes) > ", MAX_READ_LEN - ofs);
    ret = read(0, buf + ofs, MAX_READ_LEN - ofs);
    if (ret < 0)
      return 1;
    ofs += ret;
  }
  return 0;
}
