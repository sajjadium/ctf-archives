#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <string.h>

#define BUF_SIZE 32
#define MAX_DEET 20
#define BIG_BUF_SIZE 100000

char * deets[MAX_DEET];
unsigned long sizes[MAX_DEET];
char input_buf[BIG_BUF_SIZE];

int get_index() {
    for (int i = 0; i < MAX_DEET; i++) {
        if (deets[i] == NULL) {
            return i;
        }
    }
    puts("Out of space!");
    exit(-1);
}

void menu() {
  puts("1. Add deet");
  puts("2. Remove deet");
  puts("3. Edit deet");
  puts("4. View deet");
  puts("5. Exit");
}

void * add_deet(void * args) {
  unsigned long size = *(unsigned long *) args;
  int index = get_index();
  if (index < 0) {
    puts("Out of space!");
    return NULL;
  }
  deets[index] = malloc(size);
  sizes[index] = size;
  return NULL;
}

void * remove_deet(void * args) {
  unsigned long i = *(unsigned long *) args;
  if (i < MAX_DEET) {
    free(deets[i]);
    deets[i] = NULL;
    sizes[i] = 0;
  } else {
    puts("Invalid index!");
  }
  return NULL;
}

void * edit_deet(void * args) {
  unsigned long i = (unsigned long) ((void **) args)[0];
  if (i < MAX_DEET && deets[i] != NULL) {
    unsigned long sz = sizes[i];
    printf("Editing deet of size %lu\n", sz);
    memcpy(deets[i], ((void **) args)[1], sz);
    puts("Done!");
  } else {
    puts("Invalid index!");
  }
  return NULL;
}

void * view_deet(void * args) {
  unsigned long i = *(unsigned long *) args;
  if (i < MAX_DEET && deets[i] != NULL) {
    // todo ...
    puts("Viewing deet");
    puts(deets[i]);
    puts("Done!");
  } else {
    puts("Invalid index!");
  }
  return NULL;
}

int main() {
  char buf[BUF_SIZE];
  void * arr[2] = {NULL, NULL};
  setvbuf(stdout, 0, 2, 0);
  puts("deet daemon");
  menu();

  while (1) {
    unsigned long choice = 0;
    unsigned long i = 0;
    fgets(buf, BUF_SIZE, stdin);
    choice = strtoul(buf, NULL, 10);
    void * (*ptr) (void *) = NULL;
    void * args = NULL;
    switch (choice) {
      case 1:
        fgets(buf, BUF_SIZE, stdin);
        i = strtoul(buf, NULL, 10);
        ptr = add_deet;
        args = &i;
        break;
      case 2:
        fgets(buf, BUF_SIZE, stdin);
        i = strtoul(buf, NULL, 10);
        ptr = remove_deet;
        args = &i;
        break;
      case 3:
        fgets(buf, BUF_SIZE, stdin);
        i = strtoul(buf, NULL, 10);
        fgets(input_buf, BIG_BUF_SIZE, stdin);
        ptr = edit_deet;
        arr[0] = (void *) i;
        arr[1] = input_buf;
        args = arr;
        break;
      case 4:
        fgets(buf, BUF_SIZE, stdin);
        i = strtoul(buf, NULL, 10);
        ptr = view_deet;
        args = &i;
        break;
      case 5:
        puts("no more deets 4 u");
      default:
        exit(0);
    }

    pthread_t tid;
    pthread_create(&tid, NULL, ptr, args);
    pthread_detach(tid);

    sleep(3);
  }
}