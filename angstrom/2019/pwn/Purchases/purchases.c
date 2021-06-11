#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void flag() {
	system("/bin/cat flag.txt");
}

int main() {
	gid_t gid = getegid();
	setresgid(gid, gid, gid);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	char item[60];
	printf("What item would you like to purchase? ");
	fgets(item, sizeof(item), stdin);
	item[strlen(item)-1] = 0;

	if (strcmp(item, "nothing") == 0) {
		printf("Then why did you even come here? ");
	} else {
		printf("You don't have any money to buy ");
		printf(item);
		printf("s. You're wasting your time! We don't even sell ");
		printf(item);
		printf("s. Leave this place and buy ");
		printf(item);
		printf(" somewhere else. ");
	}

	printf("Get out!\n");
	return 0;
}