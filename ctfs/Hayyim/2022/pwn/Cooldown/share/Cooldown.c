#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void init() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}

void vuln() {
	char buf[0x30];
	memset(buf, 0, 0x30);
	write(1, "> ", 2);
	read(0, buf, 0x60);
}

int main(void) {
	init();
	vuln();
	exit(0);
}
