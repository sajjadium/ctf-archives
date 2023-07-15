#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <err.h>
#include <time.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <string.h>
#include <linux/seccomp.h>
#include <seccomp.h>

void setup_seccomp () {
    scmp_filter_ctx ctx;
    ctx = seccomp_init(SCMP_ACT_KILL);
    int ret = 0;
    ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    ret |= seccomp_load(ctx);
    if (ret) {
        errx(1, "seccomp failed");
    }
}

int main () {
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    char * tmp = mmap(NULL, 4096, PROT_READ | PROT_WRITE, MAP_ANON | MAP_PRIVATE, -1, 0);

    int urandom = open("/dev/urandom", O_RDONLY);
    if (urandom < 0) {
        errx(1, "open /dev/urandom failed");
    }
    read(urandom, tmp, 4);
    close(urandom);

    unsigned int offset = *(unsigned int *)tmp & ~0xFFF;
    uint64_t addr = 0x1337000ULL + (uint64_t)offset;

    char * flag = mmap((void *)addr, 4096, PROT_READ | PROT_WRITE, MAP_ANON | MAP_PRIVATE, -1, 0);
    if (flag == MAP_FAILED) {
        errx(1, "mapping flag failed");
    }

    int fd = open("flag.txt", O_RDONLY);
    if (fd < 0) {
        errx(1, "open flag.txt failed");
    }
    read(fd, flag, 128);
    close(fd);

    char * code = mmap(NULL, 0x100000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_ANON | MAP_PRIVATE, -1, 0);
    if (code == MAP_FAILED) {
        errx(1, "mmap failed");
    }

    char * stack = mmap((void *)0x13371337000, 0x4000, PROT_READ | PROT_WRITE, MAP_ANON | MAP_PRIVATE | MAP_GROWSDOWN, -1, 0);
    if (stack == MAP_FAILED) {
        errx(1, "failed to map stack");
    }

    printf("> ");
    read(0, code, 0x100000);

    setup_seccomp();

    asm volatile(
        ".intel_syntax noprefix\n"
        "mov rbx, 0x13371337\n"
        "mov rcx, rbx\n"
        "mov rdx, rbx\n"
        "mov rdi, rbx\n"
        "mov rsi, rbx\n"
        "mov rsp, 0x13371337000\n"
        "mov rbp, rbx\n"
        "mov r8,  rbx\n"
        "mov r9,  rbx\n"
        "mov r10, rbx\n"
        "mov r11, rbx\n"
        "mov r12, rbx\n"
        "mov r13, rbx\n"
        "mov r14, rbx\n"
        "mov r15, rbx\n"
        "jmp rax\n"
        ".att_syntax prefix\n"
        :
        : [code] "rax" (code)
        :
    );
}