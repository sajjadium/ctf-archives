#include <stdio.h>
#include <stdlib.h>

void cats() {
 char hmm[40];

 puts("Do you like cats?");
 int trustNoOne = 0;
 gets(hmm);

 if(trustNoOne == 0xdeadbeef) {
  puts("hmmm... alright, here's my secret:\n");
  const char* flag = getenv("FLAG");
  if (flag == NULL) {
   printf("Flag not found!\n");
   exit(0);
  }
  printf("%s\n",flag);
 } else {
  puts(">:( you're not allowed to see my secret!");
 }
}

int main() {
 setvbuf(stdout, NULL, 2, 0);
 cats();
}
