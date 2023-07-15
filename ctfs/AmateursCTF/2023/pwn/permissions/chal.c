#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <linux/seccomp.h>
#include <seccomp.h>
#include <err.h>
#include <stdio.h>
#include <stdlib.h>

void setup_seccomp () {
    scmp_filter_ctx ctx;
    ctx = seccomp_init(SCMP_ACT_KILL);
    int ret = 0;
    ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    ret |= seccomp_load(ctx);
    if (ret) {
        errx(1, "seccomp failed");
    }
}

int main () {
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    alarm(6);

    int fd = open("flag.txt", O_RDONLY);
    if (0 > fd)
        errx(1, "failed to open flag.txt");

    char * flag = mmap(NULL, 0x1000, PROT_WRITE, MAP_ANON | MAP_PRIVATE, -1, 0);
    if (flag == MAP_FAILED)
        errx(1, "failed to mmap memory");

    if (0 > read(fd, flag, 0x1000))
        errx(1, "failed to read flag");

    close(fd);

    // make flag write-only
    if (0 > mprotect(flag, 0x1000, PROT_WRITE))
        errx(1, "failed to change mmap permissions");

    char * code = mmap(NULL, 0x100000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_ANON | MAP_PRIVATE, -1, 0);
    if (code == MAP_FAILED)
        errx(1, "failed to mmap shellcode buffer");

    printf("> ");
    if (0 > read(0, code, 0x100000))
        errx(1, "failed to read shellcode");

    setup_seccomp();

    ((void(*)(char *))code)(flag);
    exit(0);
}