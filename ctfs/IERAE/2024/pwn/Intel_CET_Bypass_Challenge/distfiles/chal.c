// gcc chal.c -fno-stack-protector -static -o chal
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

void timedout(int) {
  puts("timedout");
  exit(0);
}

char g_buf[256];

int main() {
  char buf[16];
  long long int arg1 = 0;
  long long int arg2 = 0;
  void (*func)(long long int, long long int, long long int) = NULL;

  alarm(30);
  signal(SIGALRM, timedout);

  fgets(g_buf, 256, stdin); // My mercy
  fgets(buf, 256, stdin);
  if (func) func(arg1, arg2, 0);
}
