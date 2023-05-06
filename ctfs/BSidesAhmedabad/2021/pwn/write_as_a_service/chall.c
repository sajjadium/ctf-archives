#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define BUF_SIZE 0x20
#define READ_SIZE BUF_SIZE - 1

int readline(char *buf, int size) {
  for (int i = 0; i < size; i++) {
    char c;
    if (read(0, &c, 1) <= 0) _exit(0);
    if (c == '\n') return i;
    buf[i] = c;
  }
}

int menu(){
  printf(
    "0. write to local buffer\n"
    "1. write to alloced buffer\n"
    "2. write to /dev/null\n"
    "3. write to stdout\n"
    "4. exit\n"
    "> "
  );
  char buf[BUF_SIZE];
  readline(buf, 0x10);
  return atoi(buf);
}

void to_local_buf(void){
  char buf[BUF_SIZE] = {};
  while (1){
    printf("content?\n> ");
    if (0 < readline(buf, READ_SIZE)) break;
  }
}

void to_alloced_buf(void){
  char* buf;
  while (1){
    if (buf == NULL) buf = (char*)malloc(BUF_SIZE);
    printf("content?\n> ");
    if (0 < readline(buf, READ_SIZE)) break;
  }
}

void to_devnull(void){
  char buf[BUF_SIZE] = {};
  FILE* fp = fopen("/dev/null", "w");
  while (1){
    printf("content?\n> ");
    if (0 < readline(buf, READ_SIZE)) break;
  }
  fputs(buf, fp);
  fclose(fp);
}

void to_stdout(void){
  char buf[BUF_SIZE] = {};
  FILE* fp = stdout;
  while (1){
    printf("content?\n> ");
    if (read(0, buf, READ_SIZE) != -1) break;
  }
  fputs(buf, fp);
}

int main(){
  setvbuf(stdout, NULL, _IONBF, 0);
  while (1){
    switch (menu()){
      case 0:
        to_local_buf();
        break;
      case 1:
        to_alloced_buf();
        break;
      case 2:
        to_devnull();
        break;
      case 3:
        to_stdout();
        break;
      case 4:
        _exit(0);
        break;
    }
  }
}
