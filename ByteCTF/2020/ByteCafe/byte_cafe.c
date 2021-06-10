#include <stdio.h>
#include <string.h>

int main(void)
{
  int code = 0;
  char name[1000];
  
  setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  setbuf(stderr, NULL);

  puts("Welcome to Byte Café!");
  puts("What do you want to Byte today?");

  gets(name);

  if(code != 0) {
    system("cat flag.txt");
  }
}