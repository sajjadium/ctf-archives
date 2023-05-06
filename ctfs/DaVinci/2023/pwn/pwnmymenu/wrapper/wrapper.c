#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

#define PRINT(msg) puts("[+]\t" msg);

void level1(int n){
  int i;
  char cc[0x200];
  char *cc_format = "export PATH; gcc lvl1.c -o /tmp/vuln -no-pie -fno-stack-protector "
      "-D BUF_LEN=%d 2>/dev/null";

  for (i = 0 ; i < n ; i++) {
    snprintf(cc, sizeof(cc), cc_format, rand() % 0x200);

    system(cc);

    puts("---------------------");
    system("base64 /tmp/vuln");
    puts("---------------------");

    int ret = system("/tmp/vuln");
    if (!WIFEXITED(ret) || WEXITSTATUS(ret) != 0x42)
      goto FAIL;
  }

  PRINT("Level 1 finished successfully !");
  return;

FAIL:
  PRINT("You failed exploiting my program ...");
  exit(0);
}

void level2(int n){
  int i;
  char cc[0x200];
  char *cc_format = "export PATH; gcc lvl2.c -o /tmp/vuln -no-pie -fno-stack-protector "
      "-D BUF_LEN=%d -D MENU=\\'%d\\' -D SUBMENU=\\'%c\\' 2>/dev/null";

  for (i = 0 ; i < n ; i++) {
    snprintf(cc, sizeof(cc), cc_format, rand() % 0x200, rand() % 5,
            (rand() % 5) + 'a');

    system(cc);

    puts("---------------------");
    system("base64 /tmp/vuln");
    puts("---------------------");

    int ret = system("/tmp/vuln");
    if (!WIFEXITED(ret) || WEXITSTATUS(ret) != 0x42)
      goto FAIL;
  }

  PRINT("Level 2 finished successfully !");
  return;

FAIL:
  PRINT("You failed exploiting my program ...");
  exit(0);
}

void level3(int n){
  int i;
  uint64_t menu, submenu;
  char cc[0x200];
  char *cc_format = "export PATH; gcc lvl3.c -o /tmp/vuln -no-pie -fno-stack-protector "
      "-D BUF_LEN=%d -D MENU=%lld -D SUBMENU=%lld 2>/dev/null";

  for (i = 0 ; i < n ; i++) {
    menu = rand();
    menu <<= 32;
    menu |= rand();

    submenu = rand();
    submenu <<= 32;
    submenu |= rand();

    snprintf(cc, sizeof(cc), cc_format, rand() % 0x200, menu, submenu);

    system(cc);

    puts("---------------------");
    system("base64 /tmp/vuln");
    puts("---------------------");

    int ret = system("/tmp/vuln");
    if (!WIFEXITED(ret) || WEXITSTATUS(ret) != 0x42)
      goto FAIL;
  }

  PRINT("Level 3 finished successfully !");
  return;

FAIL:
  PRINT("You failed exploiting my program ...");
  exit(0);
}

void print_flag() {
  PRINT("Flag is: {}");
}

int main() {
  int seed;
  int rand_fd = open("/dev/urandom", O_RDONLY);

  read(rand_fd, &seed, sizeof(seed));

  srand(seed);

  level1(5);
  level2(5);
  level3(10);

  print_flag();
}

