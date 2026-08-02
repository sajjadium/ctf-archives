#include <stdio.h>
#include <stdlib.h>

int win() {
	system("/bin/sh");
}

int vuln() {
	char buf[32];
	gets(buf);
	printf(buf);
	fflush(stdout);
	gets(buf);
}

int main() {
	setbuf(stdout, 0x0);
	setbuf(stderr, 0x0);
	vuln();
}
