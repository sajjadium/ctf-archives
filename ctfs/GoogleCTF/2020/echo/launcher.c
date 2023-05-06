#define _GNU_SOURCE
#include <err.h>
#include <fcntl.h>
#include <stdint.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <unistd.h>

#include <stdio.h>

void execveat(int fd, char* path, char** args, char** envp, int options) {
  syscall(__NR_execveat, (uintptr_t)fd, (uintptr_t)path, (uintptr_t)args,
          (uintptr_t)envp, (uintptr_t)options);
}

int main() {
 puts("Max binary size 10MiB");
 puts("len(ELF) u32le || ELF: ");
 uint32_t len = 0;
 if (read(STDIN_FILENO, &len, sizeof(len)) != sizeof(len)) {
     err(1, "read");
 }
 if (len > 10*1024*1024) {
   errx(1, "too large");
 }
 int fd = memfd_create("bin", MFD_CLOEXEC);
 if (fd < 0) {
   err(1, "memfd_create");
 }
 size_t to_copy = len;
 while (to_copy) {
   char buf[4096];
   size_t c = sizeof(buf) < to_copy ? sizeof(buf) : to_copy;
   ssize_t r = read(STDIN_FILENO, &buf[0], c);
   if (r <= 0) {
     err(1, "read");
   }
   to_copy -= r;
   if (write(fd, &buf[0], r) != r) {
     err(1, "write");
   }
 }
 char* args[] = {"bin", NULL};
 char* envp[] = {NULL};
 execveat(fd, "", args, envp, AT_EMPTY_PATH);
 err(1, "execveat");
 return 0;
}
