#include "stdio.h"
#include <stdlib.h>

void laugh()
{
	printf("ROP detected and denied...\n");
	exit(2);
}

void win()
{
	FILE *fptr;
	char buf[28];
	// Open a file in read mode
	fptr = fopen("flag.txt", "r");
	fgets(buf, 28, fptr);
	puts(buf);
}

void pwnable()
{
	char buffer[10];
	printf(" > ");
	fflush(stdout);

	read(0, (char *)buffer, 56);

	/* Check ret */
	__asm__ __volatile__("add $0x18, %rsp;"
						 "pop %rax;"
						 "cmp $0x0401262, %rax;"
						 "jle EXIT;"
						 "cmp $0x040128a, %rax;"
						 "jg EXIT;"
						 "jmp DONE;"
						 "EXIT:"
						 "call laugh;"
						 "DONE: push %rax;");
	return;
}

int main()
{
	setbuf(stdout, NULL);

	pwnable();

	return 0;
}
