#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <sys/mman.h>

void main(int argc, char** argv){
  printf("Shellcode %s\n", argv[1]);
  int r =  mprotect((void *)((uint64_t)argv[1] & ~4095),  4096, PROT_READ | PROT_WRITE|PROT_EXEC);
  printf("%d\n", r);
  printf("Executing...\n");
  fflush(stdout);
  void (*ret)() = (void(*)())argv[1];
  ret();
}

