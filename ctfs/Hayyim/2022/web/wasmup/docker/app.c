#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <emscripten.h>

#define NOTE_LENGTH 4

char* note[NOTE_LENGTH];
size_t size[NOTE_LENGTH];

void readStr(char* label, char* buf, size_t len) {
  printf("%s>\n", label);

  for (size_t i = 0; i < len; ++i) {
    if ((buf[i] = getchar()) == '\n') {
      buf[i] = '\0';
      break;
    }
  }
}

int readInt(char* label) {
  char buf[0x10];

  readStr(label, buf, 0x10);
  return atoi(buf);
}

void printMenu() {
  puts("-----------[menu]---------");
  puts("1. create");
  puts("2. edit");
  puts("3. delete");
  puts("4. exit");
  puts("--------------------------");
}

void createNote() {
  size_t index = readInt("index");

  if (index >= NOTE_LENGTH) {
    puts("Invalid index");
    return;
  }

  size[index] = readInt("size");

  if (size[index] > 0x80) {
    puts("Invalid size");
    return;
  }

  note[index] = malloc(size[index]);

  readStr("content", note[index], size[index]);
}

void deleteNote() {
  size_t index = readInt("index");

  if (index >= NOTE_LENGTH) {
    puts("Invalid index");
    return;
  }

  if (note[index]) {
    free(note[index]);
    note[index] = NULL;
  }
}

void editNote() {
  size_t index = readInt("index");

  if (index >= NOTE_LENGTH || !note[index]) {
    puts("Invalid index");
    return;
  }

  readStr("content", note[index], size[index]);
}

int main() {
  for (;;) {
    printMenu();
    int choice = readInt("choice");

    switch (choice) {
      case 1:
        createNote();
        break;
      case 2:
        editNote();
        break;
      case 3:
        deleteNote();
        break;
      case 4:
        emscripten_run_script("process.exit(0);");
        break;
      default:
        puts("Invalid choice");
    }
  }
}
