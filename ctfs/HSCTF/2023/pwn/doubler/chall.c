#include <stdio.h>
#include <stdlib.h>

int main() {
	char flag[32];
	FILE* f = fopen("flag.txt", "r");
	if (f == NULL) {
		puts("flag.txt not found");
		return 1;
	}
	fgets(flag, 32, f);
	fclose(f);

	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 2, 0);
	printf("Input: ");
	char buffer[16];
	fgets(buffer, 16, stdin);
	int val = atoi(buffer);
	if (val < 0) {
		puts("Error: no negative numbers allowed!");
		return 1;
	}
	int doubled = 2 * val;
	printf("Doubled: %i\n", doubled);
	if (doubled == -100) {
		puts(flag);
	}
}