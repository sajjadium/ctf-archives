#include <stdio.h>
#include <stdlib.h>

void win() {
	system("/bin/cat flag.txt");
	exit(0);
}

void vuln() {
	char buf[48];
	puts("Enter the access code: ");
	gets(buf);

	if(strcmp(buf, "Sup3rs3cr3tC0de") == 0) {
		puts("Access granted!");
	}
	else {
		puts("Invalid auth.");
		exit(-1);
	}
}

int main() {
	setbuf(stdout, 0);
	setbuf(stdin, 0);
	setbuf(stderr, 0);
	vuln();
	return 0;
}
