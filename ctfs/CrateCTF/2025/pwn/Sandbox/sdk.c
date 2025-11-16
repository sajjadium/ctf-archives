#include "sdk.h"

void _start() {
    asm volatile (
        "mov %[result], %%edi\n"
        "mov $0x3c, %%eax\n"
        "syscall"
        :
        : [result] "r" (main())
    );
}

void write_all(char *buf, size_t count) {
    size_t written = 0;
    while (written < count) {
        size_t res;
        asm volatile (
            "movq %[buf], %%rsi\n"
            "movq %[count], %%rdx\n"
            "mov $1, %%rdi\n" // stdout
            "mov $1, %%eax\n"
            "syscall"
            : "=a" (res)
            : [buf] "r" (buf + written)
            , [count] "r" (count - written)
            : "rdi", "rsi", "rdx"
        );
        written += res;
    }
}

size_t read(char *buf, size_t count) {
    size_t res;
    asm volatile (
        "movq %[buf], %%rsi\n"
        "movq %[count], %%rdx\n"
        "mov $0, %%rdi\n" // stdin
        "mov $0, %%eax\n"
        "syscall"
        : "=a" (res)
        : [buf] "r" (buf)
        , [count] "r" (count)
        : "rdi", "rsi", "rdx"
    );
    return res;
}

void *malloc(size_t count) {
    return mmap(NULL, count, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
}

void *mmap(void *addr, size_t length, int prot, int flags, int fd, size_t offset) {
    void *res;
#define mmap_impl(p)              \
    asm volatile (                \
        "movq %[addr], %%rdi\n"   \
        "movq %[length], %%rsi\n" \
        "mov %[flags], %%r10d\n"  \
        "mov %[fd], %%r8d\n"      \
        "movq %[offset], %%r9\n"  \
        "mov %[prot], %%edx\n"    \
        "mov $9, %%eax\n"         \
        "syscall"                 \
        : "=a" (res)              \
        : [addr] "r" (addr)       \
        , [length] "r" (length)   \
        , [prot] "i" (p)          \
        , [flags] "r" (flags)     \
        , [fd] "r" (fd)           \
        , [offset] "r" (offset)   \
        : "rdi", "rsi", "rdx", "r10", "r8", "r9" \
    );
    switch (prot) {
        case 1: mmap_impl(1); break;
        case 2: mmap_impl(2); break;
        case 3: mmap_impl(3); break;
        default: return NULL;
    }
#undef mmap_impl
    return res;
}

void print(char *buf) {
    int len = 0;
    while (buf[len++]);
    write_all(buf, len);
}
