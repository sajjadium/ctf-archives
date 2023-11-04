#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdbool.h>
#include <sys/prctl.h>
#include <linux/seccomp.h>
#include "notmalloc.h"

#define MAX_ENTRIES 3

char* entries[MAX_ENTRIES];

void setup_buffers() {
  setbuf(stdin,NULL);
  setbuf(stdout,NULL);
  setbuf(stderr,NULL);
}

/* filter generated with seccomp-tools : https://github.com/david942j/seccomp-tools */
static void install_seccomp() {
  static unsigned char filter[] = {32,0,0,0,4,0,0,0,21,0,0,11,62,0,0,192,32,0,0,0,0,0,0,0,53,0,9,0,0,0,0,64,21,0,7,0,9,0,0,0,21,0,6,0,2,0,0,0,21,0,5,0,1,1,0,0,21,0,4,0,0,0,0,0,21,0,3,0,1,0,0,0,21,0,2,0,3,0,0,0,21,0,1,0,60,0,0,0,21,0,0,1,231,0,0,0,6,0,0,0,0,0,255,127,6,0,0,0,0,0,0,0};
  struct prog {
    unsigned short len;
    unsigned char *filter;
  } rule = {
    .len = sizeof(filter) >> 3,
    .filter = filter
  };
  if(prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) < 0) { perror("prctl(PR_SET_NO_NEW_PRIVS)"); exit(2); }
  if(prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &rule) < 0) { perror("prctl(PR_SET_SECCOMP)"); exit(2); }
}

size_t get_number() {
  size_t n = 0;
  scanf("%zu%*c",&n);
  return n;
}

size_t get_index() {
  printf("index > ");
  size_t index = get_number();
  if(index >= MAX_ENTRIES) {
    puts("invalid index");
    exit(1);
  }
  return index;
}

void menu() {
  puts("1 - create");
  puts("2 - show");
  puts("3 - delete");
  puts("4 - exit");
  printf("> ");
}

void create() {
  size_t index = get_index();

  printf("size > ");
  size_t size = get_number();
  if(!size) return;

  entries[index] = (char*) not_malloc(size);
  if(!entries[index]) {
    puts("alloc error");
    exit(1);
  }

  printf("content > ");
  fgets(entries[index],size,stdin);
}

void show() {
  size_t index = get_index();
  if(!entries[index]) {
    puts("<empty>");
  } else {
    chunk_metadata* meta = get_metadata(entries[index]);
    printf("size : %zu\n",meta->size);
    printf("content : %s\n",entries[index]);
  }
}

void delete() {
  size_t index = get_index();
  if(!entries[index]) {
    printf("no entry to delete at index %zu\n",index);
    return;
  }
  not_free(entries[index]);
  entries[index] = NULL;
}

void hack() {
  puts("Are you a h4x0r ?");
  puts("1 - yes");
  puts("2 - no");
  printf("> ");
  size_t idx = get_number();
  if(idx == 1) {
    FILE* fp = fopen("/proc/self/maps","r");
    char* line = NULL;
    size_t size = 0;
    while (getline(&line,&size,fp) != -1) {
      if( strstr(line,"rw") && (strstr(line,"libc.so.6") || strstr(line,"libnotmalloc.so")) ) {
       printf("%s",line);
      }
    }
    free(line);
    fclose(fp);
    exit(0);
  }
  puts("good.\n");
}

int main() {
  setup_buffers();
  hack();
  install_seccomp();
  while(true) {
    menu();
    size_t idx = get_number();
    switch(idx) {
      case 1:
        create();
        break;
      case 2:
        show();
        break;
      case 3:
        delete();
        break;
      case 4:
        exit(0);
        break;
      default:
        puts("invalid choice");
    }
  }
  return 0;
}
