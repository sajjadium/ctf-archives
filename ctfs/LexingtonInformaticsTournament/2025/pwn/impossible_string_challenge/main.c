#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int win() {
	char reward[64];
	int fd = open("flag.txt", O_RDONLY);
	if (fd == -1) {
		puts("An error occured. Please contact LIT support.");
		exit(1);
	}
	else {
		reward[read(fd, reward, 64) - 1] = 0;
		printf("You did it! Your reward: %s\n", reward);
		exit(0);
	}
}

int main() {
	char *buf = malloc(32);
	memset(buf, 0, 32);
	
	puts("Type a string that has 'lit' in it and does not have 'lit' in it at the same time");
	buf[read(0, buf, 32) - 1] = 0;
	
	int contains = 0;
	int notContains = strstr(buf, "lit") == NULL;
	
	for (int i = 0; i < 32 - 2; i++) {
		if (!strncmp(buf + i, "lit", 3)) contains = 1;
	}
	
	free(buf);
	
	if (contains && notContains) {
		win();
	}
	else {
		puts("Failed");
	}
	
	exit(0);
}
