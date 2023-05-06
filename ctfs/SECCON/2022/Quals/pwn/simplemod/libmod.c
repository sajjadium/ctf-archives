#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>

#define write_str(s) write(STDOUT_FILENO, s, sizeof(s)-1)

char gbuf[0x100];

static int getnline(char *buf, int size){
	int len;

	if(size <= 0 || (len = read(STDIN_FILENO, buf, size-1)) <= 0)
		return -1;

	if(buf[len-1]=='\n')
		len--;
	buf[len] = '\0';

	return len;
}

int getint(void){
	char buf[0x10] = {0};

	getnline(buf, sizeof(buf));
	return atoi(buf);
}

void modify(void){
	uint64_t ofs;

	write_str("offset: ");
	if((ofs = getint()) > 0x2000)
		return;

	write_str("value: ");
	gbuf[ofs] = getint();
}

__attribute__((naked))
void exit_imm(int status){
	asm(
		"xor rax, rax\n"
		"mov al, 0x3c\n"
		"syscall"
	   );
	__builtin_unreachable();
}
