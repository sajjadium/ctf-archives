#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>

int main(int argc, char **argv){

  setvbuf(stdout, NULL, _IONBF, 0);

  char message[64];
  char flag[64];
  char *flag_pointer = flag;

  puts("what does the cow say???");

  gid_t gid = getegid();
  setresgid(gid, gid, gid);

  FILE *file = fopen("flag.txt", "r");
  if (file == NULL) {
    printf("No flag file. Create one locally to test.");
    exit(0);
  }

  fgets(flag, sizeof(flag), file);

  printf("> ");
  fgets(message, sizeof(message), stdin);
  printf(" ");
  printf("____________________________________\n");
  printf("< ");
  printf(message);
  printf(" >\n");
  printf(" ----------------------------------\n");
  printf("        \\   ^__^\n");
  printf("         \\  (oo)\\_______\n");
  printf("            (__)\\       )\\/\\\n");
  printf("                ||----w |\n");
  printf("                ||     ||\n");
  return;
}
