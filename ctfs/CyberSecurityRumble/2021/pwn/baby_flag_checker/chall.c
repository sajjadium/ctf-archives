#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void check(const char *input, const char *secret_flag) {	
	char guess[32], flag[64];
	if (strlen(input) > sizeof(guess)) {
		puts("HACKER!");
		return;
	}

	strncpy(guess, input, sizeof(guess));
	strncpy(flag, secret_flag, sizeof(flag));
	if (!strcmp(guess, flag)) {
		printf("Well done! You got it: %s\n", flag);
	}
	else {
		printf("Wrong flag: %s\n", guess);
	}
}

int main(int argc, char** argv) {
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);

	char *secret_flag = getenv("FLAG");
	if (!secret_flag) {
		puts("Flag not found, contact challenge authors.");
		return 1;
	}

	char input[128];
	printf("Enter the flag: ");
	fgets(input, sizeof(input), stdin);
	check(input, secret_flag);

	return 0;
}
