#include <stdio.h>
#include <stdlib.h>

void win() {
	puts("congrats! here's your flag:");
	char flagbuf[64];
	FILE* f = fopen("./flag.txt", "r");
	if (f == NULL) {
		puts("flag file not found!");
		exit(1);
	}
	fgets(flagbuf, 64, f);
	fputs(flagbuf, stdout);
	fclose(f);
}

int main() {
	/* disable stream buffering */
	setvbuf(stdin,  NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);

	char name[64];

	puts("What's your name?");
	gets(name);
	printf("Why hello there %s!\n", name);

	return 0;
}