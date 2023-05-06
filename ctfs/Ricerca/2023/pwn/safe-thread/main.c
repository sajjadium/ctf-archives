#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>

pthread_t th;

#define read_n(buf, len)                              \
  {                                                   \
    ssize_t i, s;                                     \
    for (i = 0; i < len; i += s) {                    \
      s = read(STDIN_FILENO, buf + i, 0x40);          \
      if (s <= 0 || memchr(buf + i, '\n', s)) break;  \
    }                                                 \
  }

void *thread(void *_arg) {
  ssize_t len;
  char buf[0x10] = {};
  write(STDOUT_FILENO, "size: ", 6);
  read_n(buf, 0x10);
  len = atol(buf);
  write(STDOUT_FILENO, "data: ", 6);
  read_n(buf, len);
  exit(0);
}

int main() {
  alarm(180);
  pthread_create(&th, NULL, thread, NULL);
  pthread_join(th, NULL);
  return 0;
}
