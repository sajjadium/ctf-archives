#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>

int main() {
	setvbuf(stdout, NULL, _IONBF, 0);

	gid_t gid = getegid();
	setresgid(gid, gid, gid);

	char name[64];
	char book[64];

	puts("Welcome to the LIBrary in C!");
	puts("What is your name?");
	fgets(name, 64, stdin);
	// printf works just like System.out.print in Java right?
	printf("Why hello there ");
	printf(name);
	puts("And what book would you like to check out?");
	fgets(book, 64, stdin);
	printf("Your cart:\n - ");
	printf(book);
	puts("\nThat's great and all but uh...");
	puts("It turns out this library doesn't actually exist so you'll never get your book.");
	puts("Have a nice day!");
}
