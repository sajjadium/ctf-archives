#include <stdio.h>
#include <string.h>
#include <unistd.h>

struct __attribute__((__packed__)) data {
  char buff[32];
  int check;
};

void ignore(void)
{
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
}

void get_flag(void)
{
  char flag[1024] = { 0 };
  FILE *fp = fopen("flag.txt", "r");
  fgets(flag, 1023, fp);
  printf(flag);
}

int main(void) 
{
  struct data name;
  ignore(); /* ignore this function */

  printf("What's your name?\n");
  fgets(name.buff, 64, stdin);
  sleep(2);
  printf("%s nice to meet you!\n", name.buff);
  sleep(2);
  printf("Binary exploitation is the best!\n");
  sleep(2);
  printf("Memory unsafe languages rely on coders to not make mistakes.\n");
  sleep(2);
  printf("But I don't worry, I write perfect code :)\n");
  sleep(2);

  if (name.check == 0x41414141) {
    get_flag();
  }

  return 0;
}
