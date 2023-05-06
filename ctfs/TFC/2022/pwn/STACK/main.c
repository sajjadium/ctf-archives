#include <stdlib.h>
#include <stdio.h>
#include <sys/mman.h>
#include <unistd.h>
#include <string.h>

#define PAGE_SIZE 0x1000

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    
    void *shellcode = mmap(
        NULL,
        PAGE_SIZE,
        PROT_READ | PROT_WRITE | PROT_EXEC,
        MAP_PRIVATE | MAP_ANONYMOUS,
        0,
        0
    );
    if (shellcode == MAP_FAILED) {
        printf("error code 0x1, contact admin\n");
    }
    printf("hmm?\n");
    memcpy(shellcode, "\x48\x31\xc0", 3); // xorq %rax, %rax
    read(STDIN_FILENO, shellcode + 3, PAGE_SIZE);
    asm volatile(
        "xorq  %%rbx,  %%rbx ;"
        "xorq  %%rcx,  %%rcx ;"
        "xorq  %%rdx,  %%rdx ;"
        "xorq  %%rsi,  %%rsi ;"
        "xorq  %%rdi,  %%rdi ;"
        "xorq  %%rbp,  %%rbp ;"
        "xorq  %%rsp,  %%rsp ;"
        "xorq  %%r8,   %%r8  ;"
        "xorq  %%r9,   %%r9  ;"
        "xorq  %%r10,  %%r10 ;"
        "xorq  %%r11,  %%r11 ;"
        "xorq  %%r12,  %%r12 ;"
        "xorq  %%r13,  %%r13 ;"
        "xorq  %%r14,  %%r14 ;"
        "xorq  %%r15,  %%r15 ;"
        "vpxord %%zmm0, %%zmm0, %%zmm0;"
        "vmovdqa64 %%zmm0, %%zmm1;"
        "vmovdqa64 %%zmm0, %%zmm2;"
        "vmovdqa64 %%zmm0, %%zmm3;"
        "vmovdqa64 %%zmm0, %%zmm4;"
        "vmovdqa64 %%zmm0, %%zmm5;"
        "vmovdqa64 %%zmm0, %%zmm6;"
        "vmovdqa64 %%zmm0, %%zmm7;"
        "vmovdqa64 %%zmm0, %%zmm8;"
        "vmovdqa64 %%zmm0, %%zmm9;"
        "vmovdqa64 %%zmm0, %%zmm10;"
        "vmovdqa64 %%zmm0, %%zmm11;"
        "vmovdqa64 %%zmm0, %%zmm12;"
        "vmovdqa64 %%zmm0, %%zmm13;"
        "vmovdqa64 %%zmm0, %%zmm14;"
        "vmovdqa64 %%zmm0, %%zmm15;"
        "vmovdqa64 %%zmm0, %%zmm16;"
        "vmovdqa64 %%zmm0, %%zmm17;"
        "vmovdqa64 %%zmm0, %%zmm18;"
        "vmovdqa64 %%zmm0, %%zmm19;"
        "vmovdqa64 %%zmm0, %%zmm20;"
        "vmovdqa64 %%zmm0, %%zmm21;"
        "vmovdqa64 %%zmm0, %%zmm22;"
        "vmovdqa64 %%zmm0, %%zmm23;"
        "vmovdqa64 %%zmm0, %%zmm24;"
        "vmovdqa64 %%zmm0, %%zmm25;"
        "vmovdqa64 %%zmm0, %%zmm26;"
        "vmovdqa64 %%zmm0, %%zmm27;"
        "vmovdqa64 %%zmm0, %%zmm28;"
        "vmovdqa64 %%zmm0, %%zmm29;"
        "vmovdqa64 %%zmm0, %%zmm30;"
        "vmovdqa64 %%zmm0, %%zmm31;"
        "jmp *%[shellcode]"
        : : [shellcode] "r" (shellcode) : "memory"
    );
    munmap(shellcode, PAGE_SIZE);
}