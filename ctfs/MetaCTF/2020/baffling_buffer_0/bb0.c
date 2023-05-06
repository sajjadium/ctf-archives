#include <stdio.h>
#include <stdlib.h>

void vuln() {
	int isAuthenticated = 0;
	char buf[48];
	puts("Enter the access code: ");
	gets(buf);
	puts("TODO: Implement access code checking.");
	if(isAuthenticated) {
		system("/bin/cat flag.txt");
	}
	else {
		puts("Invalid auth!");
	}
}

int main() {
	setbuf(stdout, 0);
	setbuf(stdin, 0);
	setbuf(stderr, 0);
	vuln();
	return 0;
}
