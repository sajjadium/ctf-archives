#include <unistd.h>
#include <stdio.h>

int main(void) {
  char buf[0x20];
  puts("Welcome to Pwn Warmup!");
  scanf("%s", buf);
  fclose(stdout);
  fclose(stderr);
}

__attribute__((constructor))
void setup(void) {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  alarm(60);
}
