#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <seccomp.h>
#include <sys/mman.h>
#include <unistd.h>

__attribute__((constructor)) void ignore_me() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

void load_flag() {                             
    unsigned long rand_loc = (rand() %100 + 1)+0x888888;
    char *flag = (char *)rand_loc;
    syscall(0x9,rand_loc, 0x1337, 3, 0x22, 0xffffffff, 0);
    int fd = open("flag.txt", O_RDONLY);
    read(fd, flag, 100);
    close(fd);
}

void secure_binary() {
    scmp_filter_ctx ctx;
    ctx = seccomp_init(SCMP_ACT_KILL);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(access), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_load(ctx);
}

void exec_shellcode() {
  printf("Throw Your Sploit Space Hero >>> ");
  void *code = mmap(NULL, 0x1337, PROT_WRITE | PROT_EXEC, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
  read(STDIN_FILENO, code, 0x1);
  secure_binary();
  asm("xor %rax, %rax; xor %rbx, %rbx; xor %rcx, %rcx; xor %rdi,%rdi; xor %rsi,%rsi; xor %r8,%r8");
  asm("xor %r9,%r9; xor %r10,%r10; xor %r11,%r11; xor %r12,%r12; xor %r13,%r13; xor %r14,%r14; xor %r15,%r15");
  ((void (*)())code)();
}

void main(int argc, char *argv[]) {
   load_flag();
   exec_shellcode();
}
