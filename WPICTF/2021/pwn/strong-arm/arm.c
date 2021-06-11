#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int vulnerable() {
	char buffer[128];

	printf("> ");
	fflush(stdout);

	gets(buffer);

	puts("Your Input: \n");
	puts(buffer);
	fflush(stdout);
}

int main(int argc, char** argv) {
	printf("print at %p\n", printf);
	vulnerable();

	return EXIT_SUCCESS;
}
