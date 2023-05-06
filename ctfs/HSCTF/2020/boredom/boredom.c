#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <signal.h>

void setup() {
  puts("I'm currently bored out of my mind. Give me something to do!");
  setvbuf(stdin, NULL, _IONBF, NULL);
  setvbuf(stdout, NULL, _IONBF, NULL);
}

void flag() {
  FILE *f = fopen("flag.txt", "r");
  char buf[50];
  if (f == NULL) {
    puts("You're running this locally or I can't access the flag file for some reason.");
    puts("If this occurs on the remote, ping @PMP#5728 on discord server.");
    exit(1);
  }
  fgets(buf, 50, f);
  printf("Hey, that's a neat idea. Here's a flag for your trouble: %s\n",
    buf);
  puts("Now go away.");
  exit(42);
}

int main() {
  char toDo[200];
  setup();

  printf("Give me something to do: ");
  gets(toDo);
  puts("Ehhhhh, maybe later.");
  return 0;
}
