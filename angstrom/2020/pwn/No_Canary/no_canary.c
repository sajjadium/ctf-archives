#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void flag() {
	system("/bin/cat flag.txt");
}

int main() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	gid_t gid = getegid();
	setresgid(gid, gid, gid);

	puts("Ahhhh, what a beautiful morning on the farm!\n");
	puts("       _.-^-._    .--.");
	puts("    .-'   _   '-. |__|");
	puts("   /     |_|     \\|  |");
	puts("  /               \\  |");
	puts(" /|     _____     |\\ |");
	puts("  |    |==|==|    |  |");
	puts("  |    |--|--|    |  |");
	puts("  |    |==|==|    |  |");
	puts("^^^^^^^^^^^^^^^^^^^^^^^^\n");
	puts("Wait, what? It's already noon!");
	puts("Why didn't my canary wake me up?");
	puts("Well, sorry if I kept you waiting.");
	printf("What's your name? ");

	char name[20];
	gets(name);

	printf("Nice to meet you, %s!\n", name);
}
