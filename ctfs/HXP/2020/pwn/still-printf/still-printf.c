#include <stdio.h>
#include <stdlib.h>

int main() {
	char buf[0x30];
	setbuf(stdout, NULL);
	fgets(buf, sizeof(buf), stdin);
	printf(buf);
	exit(0);
}
