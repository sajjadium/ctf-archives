#include <stdio.h>
#include <string.h>

int main() {
	FILE *f;
	char flag[50];
	f = fopen("flag.txt", "r");
	fread(flag, 50, 1, f);
	strtok(flag, "\n");
	memfrob(&flag, strlen(flag));
	strfry(&flag);
	printf("Here's your encrypted flag: %s\n", &flag);
}
