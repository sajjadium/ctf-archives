#include <fcntl.h>
#include <seccomp.h>
#include <sys/mman.h>
#include <unistd.h>

// gcc no_syscalls_allowed.c -lseccomp -o no_syscalls_allowed
// socat tcp-l:1337,reuseaddr,fork exec:./no_syscalls_allowed

char flag[100];

void main(int argc, char *argv[]) {
  int fd = open("/flag.txt", O_RDONLY);
  read(fd, flag, sizeof flag);

  void *code = mmap(NULL, 0x1000, PROT_WRITE | PROT_EXEC, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
  read(STDIN_FILENO, code, 0x1000);

  if (seccomp_load(seccomp_init(SCMP_ACT_KILL)) < 0) return;

  ((void (*)())code)();
}
