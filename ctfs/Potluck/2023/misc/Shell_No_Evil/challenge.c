#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/utsname.h>
#include <unistd.h>

unsigned char kBuiltinShellcode[] = {
    0x00, 0x00, 0x11, 0x42, 0x01, 0x00, 0xfa, 0x0b,
};

void PrintCurrentArch() {
  struct utsname result;
  uname(&result);
  printf("Challenge running on %s\n", result.machine);
}

ssize_t ReadN(int fd, void *buf, size_t count) {
  size_t read_bytes = 0;
  while (read_bytes < count) {
    ssize_t ret = read(fd, buf + read_bytes, count - read_bytes);
    if (ret < 0) {
      return ret;
    }
    read_bytes += ret;
  }
  return read_bytes;
}

int main(int argc, char *argv[]) {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);

  PrintCurrentArch();

  void *page = mmap(NULL, 4096, PROT_READ | PROT_WRITE,
                    MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
  if (page == MAP_FAILED) {
    puts("mmap failed?");
    return 1;
  }
  printf("Give me a shellcode to compute A+B, size (0 to use the builtin): ");
  size_t size = 0;
  scanf("%zu", &size);
  if (size > 4096) {
    puts("too big! ❤️");
    return 1;
  }
  if (size) {
    printf("ok, give me %zu bytes of shellcode: ", size);
    if (ReadN(0, page, size) != size) {
      return 1;
    }
  } else {
    memcpy(page, kBuiltinShellcode, sizeof(kBuiltinShellcode));
  }
  if (mprotect(page, 4096, PROT_READ | PROT_EXEC) != 0) {
    puts("mprotect failed??");
    return 1;
  }

  int a = 1;
  int b = 2;
  int (*a_plus_b)(int, int) = page;
  printf("%d + %d = %d\n", a, b, a_plus_b(a, b));
  return 0;
}
