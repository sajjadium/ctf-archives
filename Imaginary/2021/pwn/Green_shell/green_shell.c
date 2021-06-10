#include <stdio.h>
#include <sys/mman.h>

int main() {
    char* shellcode = mmap((void*)0x42420000, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    puts("Let's race");
    fgets(shellcode, 0x100, stdin);
    mprotect(shellcode, sizeof(shellcode), PROT_READ | PROT_EXEC);
    ((void (*)())shellcode)();
}
