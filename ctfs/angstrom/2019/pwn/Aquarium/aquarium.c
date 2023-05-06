#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void flag() {
	system("/bin/cat flag.txt");
}

struct fish_tank {
	char name[50];
	int fish;
	int fish_size;
	int water;
	int width;
	int length;
	int height;
};


struct fish_tank create_aquarium() {
	struct fish_tank tank;

	printf("Enter the number of fish in your fish tank: ");
	scanf("%d", &tank.fish);
	getchar();

	printf("Enter the size of the fish in your fish tank: ");
	scanf("%d", &tank.fish_size);
	getchar();

	printf("Enter the amount of water in your fish tank: ");
	scanf("%d", &tank.water);
	getchar();

	printf("Enter the width of your fish tank: ");
	scanf("%d", &tank.width);
	getchar();

	printf("Enter the length of your fish tank: ");
	scanf("%d", &tank.length);
	getchar();

	printf("Enter the height of your fish tank: ");
	scanf("%d", &tank.height);
	getchar();

	printf("Enter the name of your fish tank: ");
	char name[50];
	gets(name);

	strcpy(name, tank.name);
	return tank;
}

int main() {
	gid_t gid = getegid();
	setresgid(gid, gid, gid);

	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	struct fish_tank tank;

	tank = create_aquarium();

	if (tank.fish_size * tank.fish + tank.water > tank.width * tank.height * tank.length) {
		printf("Your fish tank has overflowed!\n");
		return 1;
	}

	printf("Nice fish tank you have there.\n");

	return 0;
}