#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#define NOTE_LEN 10
#define MAX_SIZE 300

char* notes[NOTE_LEN];

void print(const char *msg) {
  write(STDOUT_FILENO, msg, strlen(msg));
}

void getstr(char *buf, unsigned size) {
  while (--size) {
    if (read(STDIN_FILENO, buf, sizeof(char)) != sizeof(char))
      exit(1);
    else if (*buf == '\n')
      break;
    buf++;
  }

  *buf = '\0';
}

unsigned getint(void) {
  char buf[0x10] = {};

  getstr(buf, sizeof(buf));
  return atoi(buf);
}

void create(void) {
  unsigned idx, size, alignment;

  print("index: ");
  if ((idx = getint()) >= NOTE_LEN) {
    print("invalid index\n");
    return;
  }

  print("size: ");
  if ((size = getint()) >= MAX_SIZE) {
    print("invalid size\n");
    return;
  }

  print("alignment: ");
  if ((alignment = getint()) >= MAX_SIZE) {
    print("invalid alignment\n");
    return;
  }

  notes[idx] = aligned_alloc(alignment, size);

  print("note: ");
  getstr(notes[idx], size);
}

void show(void) {
  unsigned idx;

  print("index: ");
  if ((idx = getint()) >= NOTE_LEN || !notes[idx]) {
    print("invalid index\n");
    return;
  }

  print(notes[idx]);
  print("\n");
}

int main(void) {
  while (1) {
    print("1. Create\n"
          "2. Show\n"
          "> ");

    switch (getint()) {
      case 1:
        create();
        break;
      case 2:
        show();
        break;
      default:
        exit(0);
    }
  }
}

__attribute__((constructor))
static void init(void) {
  alarm(180);
}
