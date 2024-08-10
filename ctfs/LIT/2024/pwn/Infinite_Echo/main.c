#include <stdio.h>
#include <unistd.h>

int main() {
	setbuf(stdout, 0x0);
	setbuf(stderr, 0x0);
	
	char buf[256];
	
	printf("Infinite Echo!\n");
	while (1 == 1) {
		buf[read(0, buf, 256) - 1] = 0;
		printf(buf);
		printf("\n");
	}
}
