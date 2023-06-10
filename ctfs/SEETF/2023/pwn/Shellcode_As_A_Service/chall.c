// gcc chall.c -o chall -lseccomp

#define _GNU_SOURCE 1

#include <sys/mman.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <assert.h>
#include <unistd.h>
#include <stdio.h>
#include <seccomp.h>

void *shellcode_mem;
size_t shellcode_size;

int main(int argc, char **argv, char **envp)
{
    shellcode_mem = mmap((void *) 0x1337000, 0x1000, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE|MAP_ANON, 0, 0);
    assert(shellcode_mem == (void *) 0x1337000);

    puts("Welcome to the SEETF shellcode sandbox!");
    puts("======================================");
    puts("Allowed syscalls: open, read");
    puts("You've got 6 bytes, make them count!");
    puts("======================================");
    fflush(stdout);

    shellcode_size = read(0, shellcode_mem, 0x6);
    assert(shellcode_size > 0);

    scmp_filter_ctx ctx;
    ctx = seccomp_init(SCMP_ACT_KILL);

    assert(seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0) == 0);    
    assert(seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0) == 0);

    assert(seccomp_load(ctx) == 0);

    ((void(*)())shellcode_mem)();
}