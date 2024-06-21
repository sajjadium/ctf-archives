#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NOTE_LIST_LEN 16
#define MAX_NOTE_SIZE 4096

void init() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  alarm(180);
}

typedef struct note {
  int size;
  char *ptr;
} note_t;

note_t list[NOTE_LIST_LEN];
note_t copied;

void menu() {
  printf("\n---- memu ----\n");
  printf("1. create note\n");
  printf("2. show note\n");
  printf("3. copy note\n");
  printf("4. paste note\n");
  printf("5. delete note\n");
  printf("6. exit\n");
  printf("--------------\n\n");
}

int get_idx() {
  int idx;
  printf("index: ");
  if ((scanf("%d", &idx) != 1) || idx < 0 || idx >= NOTE_LIST_LEN) {
    printf("Invalid index!\n");
    return -1;
  }
  return idx;
}

int get_size() {
  int size;
  printf("size (0-%d): ", MAX_NOTE_SIZE);
  if ((scanf("%d", &size) != 1) || size < 0 || size > MAX_NOTE_SIZE) {
    printf("Invalid size!\n");
    return -1;
  }
  return size;
}

int is_empty(int idx) {
  int f = (list[idx].ptr == NULL);
  if (f)
    printf("The note is empty!\n");
  return f;
}

void create() {
  int idx, size;
  if ((idx = get_idx()) == -1)
    return;
  if ((size = get_size()) == -1)
    return;
  list[idx].size = size;
  list[idx].ptr = (char *)malloc(list[idx].size);
  memset(list[idx].ptr, 0, list[idx].size);
  printf("Enter your content: ");
  read(0, list[idx].ptr, list[idx].size);
  printf("Done!\n");
}

void show() {
  int idx;
  if ((idx = get_idx()) == -1)
    return;
  if (is_empty(idx))
    return;
  write(1, list[idx].ptr, list[idx].size);
}

void copy() {
  int idx;
  if ((idx = get_idx()) == -1)
    return;
  if (is_empty(idx))
    return;
  copied = list[idx];
  printf("Done!\n");
}

void paste() {
  int idx;
  note_t pasted;
  if ((idx = get_idx()) == -1)
    return;
  if (is_empty(idx))
    return;
  if (copied.ptr == NULL) {
    printf("Please copy a note before pasting!\n");
    return;
  }
  pasted.size = list[idx].size + copied.size;
  if (pasted.size < 0 || pasted.size > MAX_NOTE_SIZE) {
    printf("Invalid size!\nPaste failed!\n");
    return;
  }
  pasted.ptr = (char *)malloc(pasted.size);
  memset(pasted.ptr, 0, pasted.size);
  sprintf(pasted.ptr, "%s%s", list[idx].ptr, copied.ptr);
  free(list[idx].ptr);
  list[idx] = pasted;
  printf("Done!\n");
}

void delete () {
  int idx;
  if ((idx = get_idx()) == -1)
    return;
  if (is_empty(idx))
    return;
  free(list[idx].ptr);
  list[idx].size = 0;
  list[idx].ptr = NULL;
  printf("Done!\n");
}

int main() {
  init();
  int c = 0;

  while (1) {
    menu();
    printf("your choice: ");
    scanf("%d", &c);

    if (c == 1)
      create();
    else if (c == 2)
      show();
    else if (c == 3)
      copy();
    else if (c == 4)
      paste();
    else if (c == 5)
      delete ();
    else if (c == 6)
      return 0;
    else
      printf("Invalid choice!\n");

    scanf("%*[^\n]"); // fflush stdin
  }
  return 0;
}
