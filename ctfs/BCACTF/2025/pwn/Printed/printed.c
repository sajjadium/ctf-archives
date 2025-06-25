#include <stdio.h>

char flag[128];

void show(char* name, char* flag) {
	char newflag[50];
	snprintf(newflag, sizeof(newflag), name);
	printf("%s", newflag);
}

int main() {
	char name[45];
	printf(" > What's your name?  ");
	fgets(name, 45, stdin);
	
	FILE *fp = fopen("flag.txt", "r");
	if (fp) {
		fgets(flag, sizeof(flag), fp);
		fclose(fp);
	} else {
		flag[0] = '\0';
	}

	show(name, flag);

	return 0;
}

