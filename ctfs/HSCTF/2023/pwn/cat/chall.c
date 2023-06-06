#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 2, 0);

	char flag[19];
	FILE* f = fopen("flag.txt", "r");
	if (f == NULL) {
		puts("flag.txt not found");
		return 1;
	}
	fgets(flag, 19, f);
	fclose(f);

	char buffer[16];
	while (1) {
		fgets(buffer, 16, stdin);
		printf(buffer);
	}
}