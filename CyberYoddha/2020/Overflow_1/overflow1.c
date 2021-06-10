#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
  char str[] = "AAAA";
  char buf[16];

  gets(buf);
  
  if (!(str[0] == 'A' && str[1] == 'A' && str[2] == 'A' && str[3] == 'A')){
    system("/bin/sh");
  }
}
