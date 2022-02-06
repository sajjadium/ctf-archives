#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/prctl.h>
#include <linux/filter.h>
#include <linux/seccomp.h>

uint8_t *chunk = 0;

void seccomp()
{
    struct sock_filter filter[] = {
        {0x20, 0, 0, 0x00000004},
        {0x15, 0, 11, 0xc000003e},
        {0x20, 0, 0, 0x00000000},
        {0x15, 8, 0, 0x00000000},
        {0x15, 7, 0, 0x00000001},
        {0x15, 6, 0, 0x00000002},
        {0x15, 5, 0, 0x0000003c},
        {0x15, 4, 0, 0x000000e7},
        {0x15, 1, 0, 0x00000009},
        {0x5, 0, 0, 0x00000003},
        {0x20, 0, 0, 0x00000020},
        {0x45, 1, 0, 0x00000004},
        {0x6, 0, 0, 0x7fff0000},
        {0x6, 0, 0, 0x00000000},
    };

    struct sock_fprog prog = {
        .len = (sizeof(filter)) / sizeof(struct sock_filter),
        filter,
    };

    prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
    prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog);
}

void __attribute__((constructor)) nightmare()
{
    if (!chunk)
    {
        chunk = malloc(0x40000);
        seccomp();
    }
    uint8_t byte = 0;
    size_t offset = 0;

    read(0, &offset, sizeof(size_t));
    read(0, &byte, sizeof(uint8_t));

    chunk[offset] = byte;

    write(1, "BORN TO WRITE WORLD IS A CHUNK 鬼神 LSB Em All 1972 I am mov man 410,757,864,530 CORRUPTED POINTERS", 101);
    _Exit(0);
}

int main()
{
    _Exit(0);
}
