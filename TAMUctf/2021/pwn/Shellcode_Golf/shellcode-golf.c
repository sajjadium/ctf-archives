#include <stdlib.h>
#include <stdio.h>
#include <sys/mman.h>

char* get_flag() {
	FILE* flag = fopen("flag.txt", "r");
	char* buf = malloc(64);
	if(flag == NULL) {
		exit(1);
	} else {
		fgets(buf, 64, flag);
	}
	return buf;
	fflush(0);
}

void main() {
	char* flag = get_flag();
	char* shellcode = (char*) mmap((void*) 0x1337,12, 0, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
	mprotect(shellcode, 12, PROT_READ | PROT_WRITE | PROT_EXEC);
	fgets(shellcode, 12, stdin);
	((void (*)(char*))shellcode)(flag);
}