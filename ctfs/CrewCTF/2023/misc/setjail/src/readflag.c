#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
  char flag[256] = {0};
  
  if (argc != 2) {
    printf("Usage: %s givemeflag\n", argv[0]);
    return 1;
  };

  if (strcmp(argv[1], "givemeflag")) {
    puts("Incorrect password");
    return 1;
  };

  puts("dummy{dummy}");
  
  return 0;
}
