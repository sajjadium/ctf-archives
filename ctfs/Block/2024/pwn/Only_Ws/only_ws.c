#include <seccomp.h>
#include <syscall.h>

#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>

#include <string.h>

typedef void shellcode();
char flag[64];

int main(int argc, char **argv) {
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  FILE *f = fopen("flag.txt", "r");
  if (f == NULL) {
    printf("error reading flag");
    return -1;
  }

  fscanf(f, "%s", flag);
  printf("Flag is at 0x%x\n", (void *)flag);
  fclose(f);

  char shellcode_buf[4096];
  int bytes_read = read(STDIN_FILENO, shellcode_buf, sizeof(shellcode_buf));

  void *shellcode_ptr =
      mmap((void *)shellcode_buf, 1, PROT_READ | PROT_WRITE | PROT_EXEC,
           MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
  memcpy(shellcode_ptr, shellcode_buf, bytes_read);

  scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL_PROCESS);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);

  seccomp_load(ctx);
  seccomp_release(ctx);
  ((shellcode *)shellcode_ptr)();
}
