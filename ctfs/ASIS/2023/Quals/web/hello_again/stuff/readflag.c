#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
  char flag[256] = {0};

  if(argc != 2 || strcmp(argv[1],"gimmeflag")){
    puts("Run `/readflag gimmeflag`");
    return 1;
  }
  FILE* fp = fopen("/flag.txt", "r");
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