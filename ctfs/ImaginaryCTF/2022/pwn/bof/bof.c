#include <stdio.h>
#include <stdlib.h>

struct string {
  char buf[64];
  int check;
};

char temp[1337];


int main() {
  struct string str;

  setvbuf(stdout,NULL,2,0);
  setvbuf(stdin,NULL,2,0);

  str.check = 0xdeadbeef;
  puts("Enter your string into my buffer:");
  fgets(temp, 5, stdin);
  sprintf(str.buf, temp);

  if (str.check != 0xdeadbeef) {
    system("cat flag.txt");
  }
}

