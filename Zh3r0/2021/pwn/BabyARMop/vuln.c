#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void vuln() {
	char name_buffer[0x20];
	read(0, name_buffer, 0x1f);
	printf("Hello, %s\n; send me your message now: ", name_buffer);
	fflush(stdout);
	read(0, name_buffer, 0x200);
}

int main() {
	printf("Enter your name: ");
	fflush(stdout);
	vuln();
	return 0;
}
