#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <stdlib.h>

#ifndef ALLOCATION_SIZE
#define ALLOCATION_SIZE 65536
#endif

#ifndef CODE_FILE
#define CODE_FILE "/src/glitter-printer"
#endif

int main(int argc, char *argv[]){
  struct stat statbuf;
  if(stat(CODE_FILE, &statbuf) == -1) {
    fprintf(stderr, "Error reading code file: "CODE_FILE"\n");
    exit(0);
  }

  if(ALLOCATION_SIZE < statbuf.st_size) {
    fprintf(stderr, "Size must be at least %ld (ALLOCATION_SIZE is %d)\n", statbuf.st_size, ALLOCATION_SIZE);
    exit(0);
  }

  void *a = mmap(0, ALLOCATION_SIZE, PROT_EXEC |PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_SHARED, -1, 0);
  //fprintf(stderr, "allocated %zd bytes of executable memory at: %p\n", ALLOCATION_SIZE, a);

  FILE *file = fopen(CODE_FILE, "rb");
  if(read(fileno(file), a, statbuf.st_size) != statbuf.st_size)
  {
    fprintf(stderr, "Failed to read() the entire file!\n");
    exit(1);
  }

  /* Give it 60 seconds to run before killing the process with SIGALRM */
  alarm(60);

  /* Jump to the start, losing the return address to the void of space */
  __asm__("jmp *%0\n" : :"r"(a));
}
