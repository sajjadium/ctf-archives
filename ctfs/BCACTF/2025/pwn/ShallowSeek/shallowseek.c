#include <stdio.h>
#include <string.h>

char *welcome = "Welcome to ShallowSeek!\nShallowSeek is a new, hyperadvanced AI that can answer any of your questions (that comply with government rules)! Ask away!\n";
char *begin = "Sorry, but \"";
char *end = "\" is beyond my current scope. Let's talk about something else.\n";

int main(int argc, char **argv) {
	setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

	char input[64];
	char flag[64];
	fgets(flag, 64, fopen("flag.txt", "r"));
	printf("%s", welcome);
	while (1) {
		// read input
		int i = 0;
		char c;
		while ((c = getchar()) != '\n') {
			input[i++] = c;
		};

		// no buffer overflow for you
		if (strlen(input) == 64) {
			printf("%s", "Invalid input: use less than 64 characters");
			continue;
		}
		
		// print out censored results (gov. banned everything whoops)
		printf("%s", begin);
		printf("%s", input);
		printf("%s", end);

		// clear input
		for (int j = 0; j < 64; j++) {
			input[j] = 0;
		}
	}
	return 0;
}
