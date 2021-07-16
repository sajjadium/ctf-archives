#include <stdio.h>
#include <stdlib.h>

int main(){
	setbuf(stdout, 0x0);
	setbuf(stderr, 0x0);

	puts("Do you have any complaints about this lazily written problem?");

	int buf[0x80];
	buf[read(0x0, buf, 0x79)] = '\0';

	puts("You said:");
	printf(buf);

	puts("Your criticism will be taken into consideration.");

	return 0;
}
