#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int win() {
	system("/bin/sh");
}

int main() {
	setbuf(stdout, 0);
	setbuf(stderr, 0);
	char buf[256];
	long x = 0;
	printf("Buffer located at: %p\n", buf);
	buf[read(0, buf, 256) - 1] = 0;
	printf(buf);
	if (x) win();
	exit(0);
}
