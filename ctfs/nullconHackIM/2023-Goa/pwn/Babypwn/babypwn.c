#include <stdio.h>
#include <unistd.h>

int main() {
   setbuf(stdout, NULL);

   char username[512];

   printf("You shell play a game against @gehaxelt! Win it to get ./flag.txt!\n");
   printf("Your game slot is at: %p\n", username);
   printf("What's your name?\n");
   read(1, username, 1024);
   printf("Ok, it's your turn, %s!\n", username);
   printf("You lost! Sorry :-(\n");

   return 0;
}