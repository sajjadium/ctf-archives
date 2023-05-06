#include <stdio.h>

int main(void) {
  char flag[256] = {0};
  FILE* fp = fopen("/flag", "r");
  if (!fp) {
    perror("fopen");
    return 1;
  }
  if (fread(flag, 1, 256, fp) < 0) {
    perror("fread");
    return 1;
  }
  puts(flag);
  fclose(fp);
  return 0;
}