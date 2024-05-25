#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main() {
	gid_t gid = getegid();
	setresgid(gid, gid, gid);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	char item[50];
	printf("What item would you like to return? ");
	fgets(item, 50, stdin);
	item[strlen(item)-1] = 0;

	if (strcmp(item, "nothing") == 0) {
		printf("Then why did you even come here? ");
	} else {
		printf("We didn't sell you a ");
		printf(item);
		printf(". You're trying to scam us! We don't even sell ");
		printf(item);
		printf("s. Leave this place and take your ");
		printf(item);
		printf(" with you. ");
	}

	printf("Get out!\n");
	return 0;
}