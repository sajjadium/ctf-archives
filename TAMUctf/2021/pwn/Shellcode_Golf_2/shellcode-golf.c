#include <stdlib.h>
#include <stdio.h>
#include <sys/mman.h>

void main() {
	char* shellcode = (char*) mmap((void*) 0x1337, 7, 0, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
	mprotect(shellcode, 7, PROT_READ | PROT_WRITE | PROT_EXEC);
	fgets(shellcode, 7, stdin);
	((void (*)())shellcode)();
}
