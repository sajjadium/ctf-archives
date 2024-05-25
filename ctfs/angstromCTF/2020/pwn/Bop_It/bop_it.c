#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include <string.h>

int main() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	gid_t gid = getegid();
	setresgid(gid, gid, gid);

	const char *actions[] = {"Bop it!\n", "Twist it!\n", "Pull it!\n", "Flag it!\n"};

	srand(time(NULL));

	char c;
	char *action = actions[rand()%4];
	write(1, action, strlen(action));
	while ((c = getchar()) != EOF) {
		if (!strcmp(action, actions[3])) {
			char guess[256];
			guess[0] = c;
			int guessLen = read(0, guess+1, 255)+1; //add to already entered char
			guess[guessLen-1] = 0; //remove newline
			char flag[32];
			FILE *f = fopen("flag.txt", "rb");
			int r = fread(flag, 1, 32, f);
			flag[r] = 0; //null terminate
			if (strncmp(guess, flag, strlen(flag))) {
				char wrong[strlen(guess)+35];
				wrong[0] = 0; //string is empty intially
				strncat(wrong, guess, guessLen);
				strncat(wrong, " was wrong. Better luck next time!\n", 35);
				write(1, wrong, guessLen+35);
				exit(0);
			}
		} else if (c != action[0]) {
			char wrong[64] = "_ was wrong. What you wanted was _!\n";
			wrong[0] = c; //user inputted char
			wrong[strlen(wrong)-3] = action[0]; //correct char
			write(1, wrong, strlen(wrong));
			getchar(); //so there's no leftover newline
			exit(0);
		} else { getchar(); }
		action = actions[rand()%4];
		write(1, action, strlen(action));
	}
}
