#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>

void code_runner()
{
	char tmp_code[18];
	char *code;
	bool executing = false;

	printf("Please enter your code: ");
	fflush(stdout);

	fgets(tmp_code, 17, stdin);

	char *end = strchr(tmp_code, '\n');
	if (end == NULL) end = &tmp_code[16];
	*end = '\0';
	int len = end - tmp_code;

	/* NO KERNEL FUNCS */
	if (strstr(tmp_code, "\xcd\x80") || strstr(tmp_code, "\x0f\x34") || strstr(tmp_code, "\x0f\x05"))
	{
		printf("Nice try, but syscalls aren't permitted\n");
		return;
	}

	/* NO CALLS TO DYNAMIC ADDRESSES */
	if (strstr(tmp_code, "\xff"))
	{
		printf("Nice try, but dynamic calls aren't permitted\n");
		return;
	}

	code = mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
	memcpy(code, tmp_code, len);
	code[len] = 0xc3;

	mprotect(code, 4096, PROT_READ|PROT_EXEC);
	if (executing == true)
	{
		printf("ROP chain detected!\n");
		munmap(code, 4096);
		exit(-1);
	}

	void (*func)() = (void (*)())code;
	executing = true;
	func();

	munmap(code, 4096);
}

int main(int argc, char **argv)
{
	gid_t gid = getegid();
	setresgid(gid,gid,gid);

	printf("Welcome to the Executor\n");
	code_runner();

	return 0;
}
