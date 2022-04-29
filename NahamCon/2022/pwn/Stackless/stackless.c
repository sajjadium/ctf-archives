#include <seccomp.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

void timeout(int _sig) {
    _exit(EXIT_SUCCESS);
}

void sandbox(void) {
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL_PROCESS);
    if (!ctx) {
        perror("seccomp_init");
        _exit(EXIT_FAILURE);
    }

    if (seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0) < 0) {
        perror("seccomp_rule_add(..., SCMP_SYS(exit), ...)");
        _exit(EXIT_FAILURE);
    }

    if (seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0) < 0) {
        perror("seccomp_rule_add(..., SCMP_SYS(exit_group), ...)");
        _exit(EXIT_FAILURE);
    }

    if (seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0) < 0) {
        perror("seccomp_rule_add(..., SCMP_SYS(read), ...)");
        _exit(EXIT_FAILURE);
    }

    if (seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0) < 0) {
        perror("seccomp_rule_add(..., SCMP_SYS(write), ...)");
        _exit(EXIT_FAILURE);
    }

    if (seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0) < 0) {
        perror("seccomp_rule_add(..., SCMP_SYS(open), ...)");
        _exit(EXIT_FAILURE);
    }

    if (seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(close), 0) < 0) {
        perror("seccomp_rule_add(..., SCMP_SYS(close), ...)");
        _exit(EXIT_FAILURE);
    }

    if (seccomp_load(ctx) < 0) {
        perror("seccomp_load");
        _exit(EXIT_FAILURE);
    }

    seccomp_release(ctx);
}

int main(void) {
    FILE *fp = NULL;
    unsigned int seed = 0;
    void *code = (void *)-1;
    size_t shellcode_len = 0;
    size_t addr = 0;
    int attempts = 0;
    unsigned char ops[] = {0x4d, 0x31, 0xff};

    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    if ((fp = fopen("/dev/urandom", "r")) == NULL) {
        perror("fopen");
        return EXIT_FAILURE;
    }

    if (fread(&seed, sizeof(seed), 1, fp) != 1) {
        perror("fread");
        return EXIT_FAILURE;
    }

    fclose(fp);
    srand(seed);

    for (int attempts = 0; attempts < 10 && code == (void *)-1; attempts++) {
        addr = (unsigned int)rand() & ~0xfff;
        addr |= (size_t)(rand() & 0xffff) << 32;

        code = mmap((void *)addr, 0x1000, PROT_READ | PROT_WRITE,
                    MAP_ANONYMOUS | MAP_PRIVATE | MAP_FIXED, 0, 0);
    }

    if (attempts == 10) {
        perror("mmap");
        return EXIT_FAILURE;
    }

    memcpy(code, ops, sizeof(ops));

    puts("Shellcode length");
    scanf("%zu", &shellcode_len);
    getchar();

    shellcode_len = shellcode_len > (0x1000 - sizeof(ops))
                        ? 0x1000 - sizeof(ops)
                        : shellcode_len;

    puts("Shellcode");
    read(STDIN_FILENO, code + sizeof(ops), shellcode_len);

    if (mprotect(code, 0x1000, PROT_READ | PROT_EXEC) != 0) {
        perror("mprotect");
        return EXIT_FAILURE;
    }

    signal(SIGALRM, timeout);
    alarm(60);
    sandbox();

    __asm__ volatile(".intel_syntax noprefix\n"
                     "mov r15, %[addr]\n"
                     "xor rax, rax\n"
                     "xor rbx, rbx\n"
                     "xor rcx, rcx\n"
                     "xor rdx, rdx\n"
                     "xor rsp, rsp\n"
                     "xor rbp, rbp\n"
                     "xor rsi, rsi\n"
                     "xor rdi, rdi\n"
                     "xor r8, r8\n"
                     "xor r9, r9\n"
                     "xor r10, r10\n"
                     "xor r11, r11\n"
                     "xor r12, r12\n"
                     "xor r13, r13\n"
                     "xor r14, r14\n"
                     "jmp r15\n"
                     ".att_syntax"
                     :
                     : [addr] "r"(code));

    return EXIT_SUCCESS;
}
