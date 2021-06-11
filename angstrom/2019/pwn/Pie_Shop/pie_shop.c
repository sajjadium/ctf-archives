#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void flag() {
	system("/bin/cat flag.txt");
}

void get_pie() {
	printf("What type of pie do you want? ");

	char pie[50];
	gets(pie);

	if (strcmp(pie, "apple") == 0) {
		printf("Here's your pie!\n");
		printf("      _,..---..,_\n");
		printf("  ,-\"`    .'.    `\"-,\n");
		printf(" ((      '.'.'      ))\n");
		printf("  `'-.,_   '   _,.-'`\n");
		printf("    `\\  `\"\"\"\"\"`  /`\n");
		printf("      `\"\"-----\"\"`\n");
	} else {
		printf("Whoops, looks like we're out of that one.\n");
	}
}

int main() {
	gid_t gid = getegid();
	setresgid(gid, gid, gid);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	printf("Welcome to the pie shop! Here we have all types of pies: apple pies, peach pies, blueberry pies, position independent executables, pumpkin pies, rhubarb pies...\n");
	get_pie();

	return 0;
}