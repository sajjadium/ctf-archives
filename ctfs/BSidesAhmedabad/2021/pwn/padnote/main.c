#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define CHECK_FAIL(ERR) {                       \
    puts(ERR);                                  \
    return;                                     \
  }

#define MAX_NOTE 4

typedef struct {
  int size;
  char *content;
} Note;

Note noteList[MAX_NOTE];

void ReadLine(char *buf, int size) {
  char c;

  for (int i = 0; i != size - 1; i++) {
    if (read(0, &c, sizeof(c)) < 0)
      exit(1); // IO error
    if (c == '\n')
      break;
    else
      buf[i] = c;
  }
}

void CreateNote(Note *note) {
  int size;
  char *content;

  /* Check if note is empty */
  if (note->content)
    CHECK_FAIL("Note is in use");

  /* Input data length */
  printf("Size: ");
  if (scanf("%d%*c", &size) <= 0)
    exit(0); // IO error

  /* Security check */
  if (size <= 0)
    CHECK_FAIL("Size must be larger than 0");

  /* Initialize note */
  if (!(content = (char*)calloc(sizeof(char), size)))
    CHECK_FAIL("Could not allocate the memory");

  /* Input content */
  printf("Content: ");
  ReadLine(content, size);

  note->content = content;
  note->size = size;
}

void EditNote(Note *note) {
  int offset, count, epos;

  /* Check if note is empty */
  if (!note->content)
    CHECK_FAIL("Note is empty");

  /* Input offset */
  printf("Offset: ");
  if (scanf("%d%*c", &offset) <= 0)
    exit(0); // IO error

  /* Input count */
  printf("Count: ");
  if (scanf("%d%*c", &count) <= 0)
    exit(0); // IO error

  /* Security check */
  if (offset < 0)
    CHECK_FAIL("Invalid offset");
  if (count <= 0)
    CHECK_FAIL("Invalid count");
  if ((epos = offset + count) < 0)
    CHECK_FAIL("Integer overflow");
  if (epos > note->size)
    CHECK_FAIL("Out-of-bound access");
  
  /* Edit content */
  printf("Content: ");
  ReadLine(&note->content[offset], count);
}

void PrintNote(Note *note) {
  /* Check if note is empty */
  if (!note->content)
    CHECK_FAIL("Note is empty");

  /* Print note */
  printf("Content: ");
  if (write(1, note->content, note->size) <= 0)
    exit(0); // IO error
  putchar('\n');
}

void DeleteNote(Note *note) {
  /* Check if note is empty */
  if (!note->content)
    CHECK_FAIL("Note is empty");

  /* Delete note */
  free(note->content);
  note->size = 0;
  note->content = NULL;
}

int main() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  alarm(180);

  puts("1. CreateNote");
  puts("2. EditNote");
  puts("3. PrintNote");
  puts("4. DeleteNote");
  while (1) {
    int choice, index;

    /* Input choice */
    printf("Choice: ");
    if (scanf("%d%*c", &choice) <= 0)
      exit(0);
    if (choice < 1 || choice > 4) {
      puts("Bye!");
      return 0;
    }

    /* Input index */
    printf("Index: ");
    if (scanf("%d%*c", &index) <= 0)
      exit(0);

    /* Security check */
    if (index < 0 || index >= MAX_NOTE) {
      puts("Invalid index");
      continue;
    }

    switch (choice) {
    case 1: CreateNote(&noteList[index]); break;
    case 2: EditNote(&noteList[index]); break;
    case 3: PrintNote(&noteList[index]); break;
    case 4: DeleteNote(&noteList[index]); break;
    }
  }
}
