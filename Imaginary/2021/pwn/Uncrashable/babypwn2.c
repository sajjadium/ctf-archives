#include <stdio.h>
#include <signal.h>

#define LEN 100

void getflag(int signum) {
	FILE* f = fopen("/tmp/flag2", "r");
	char flag[50];
	fscanf(f, "%s", flag);
	printf("Error %d: %s\n", signum, flag);
	fclose(f);
	exit(signum);
}

int vuln(int a, long b) {
	int very_important_information[LEN];
	char input[LEN]; //having extra bytes for input perfectly completely protects against buffer overflow attacks!

	for (int i = 0; i < LEN; i++) {
		very_important_information[i] = a^(int)(b&0xffffffff);
		a = a ^ (b >> 32);
	}
	printf("This is a very secure and foolproof server, which is very important, because if this server broke, very bad things would happen.\n");
	printf("Please enter an address for the information you would like to retrieve. The first 8 bytes entered will be treated as the address. Large addresses will be truncated.\n\n");
	printf("Address: ");
	gets(input);
	unsigned long addr = input[0];
	for (int i = 1; i < 8; i++){
		addr <<= 8;
		addr += input[i];
	}
	addr = (addr % LEN) * (addr > 0);
	printf("Here is your very important information: 0x%x.\n", very_important_information[addr]);	
	printf("Goodbye!\n");
}

int main() {
	setbuf(stdout, NULL);
	signal(SIGSEGV, getflag);
	vuln(0xdeadface, 0x1337133713371337);
}