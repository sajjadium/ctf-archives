#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

struct weeb {
	char name[50];
	double days_of_anime;
};

struct weeb weebs[6];

struct weapon {
	char name[100];
	int id;
};

struct weapon* inventory[10];

const char* const actions[4] = {
	"You slash the weeb's arm off. \"'tis but a scratch,\" he claims, but it's obviously a little worse than that. In the intense pain, he has forgotten 8 days worth of anime.",
	"You blow into the whistle and the piercing sound engulfs the weeb's sensory system. He forgets 6 days worth of anime.",
	"You bop the weeb on the head with the rolled up newspaper. He suffers minor brain damage and forgets a single day of anime.",
	"" // TODO: come up with action
};

const char* const prompts[5] = {
	"A soft light emanates from above. All around you are trees, several times your height.",
	"You hear footsteps nearby, but you can't quite make out where they're coming from.",
	"A foreboding feeling washes over you. \"This can't be good,\" you think.",
	"You hear foreign babbling from all directions, sending chills down your spine.",
	"The forest has turned dark. You can barely make out your surroundings.",
};

const char* const items[4] = {
	"sword",
	"whistle",
	"newspaper",
	"fist"
};

const int damages[4] = {
	8,
	6,
	1,
	5
};

void initialize_weeb(int i, char name[], double days) {
	strcpy(weebs[i].name, name);
	weebs[i].days_of_anime = days;
}

void initialize_weebs() {
	initialize_weeb(0, " arxenix", 42.7);
	initialize_weeb(1, " notjagan", 46.7);
	initialize_weeb(2, " neptunia", 44.2);
	initialize_weeb(3, " hanto", 70.2);
	initialize_weeb(4, " slenderestman", 20.7);
	initialize_weeb(5, " VoidMercy", 53);
}

void fight_weeb() {
	int id = rand() % 6;
	fflush(stdout);
	printf("You hear a noise behind you... \"BAKA!!!\"%s comes charging at you. You check your inventory for a weapon.\n", weebs[id].name);
	for (int i = 0; i < 10; i++) {
		if (inventory[i] && inventory[i]->id < 3) {
			printf("%d. %s\n", i+1, inventory[i]->name);
		} else {
			printf("%d. empty\n", i+1);
		}
	}
	int slot = -1;
	while (slot < 1 || slot > 10) {
		printf("Which weapon would you like to use? ");
		scanf("%d", &slot);
	}
	getchar();
	slot = slot - 1;
	if (inventory[slot] == 0) {
		printf("You grasp for your weapon, but you can't find anything. The slot is empty!%s begins watching anime in front of you and you become entranced. Otaku, kawaii, senpai... you have become one of them.\n", weebs[id].name);
		exit(0);
	}
	printf("%s\n", actions[(inventory[slot]->id)]);
	weebs[id].days_of_anime = weebs[id].days_of_anime - damages[inventory[slot]->id];
	printf("The weeb recovers quickly and prepares to strike back.\nKnowing you have no chance of defeating someone who's watched %.1f days of anime, you run away as fast as you can. In your haste, you leave your %s behind.\n", weebs[id].days_of_anime, items[inventory[slot]->id]);
	inventory[slot]->id = 3;
	free(inventory[slot]);
}

void find_item() {
	struct weapon** item = 0;
	for (int i = 0; i < 10; i++) {
		if (inventory[i] == 0 || inventory[i]->id >= 3) {
			item = &inventory[i];
			break;
		}
	}
	int id = rand() % 3;
	if (item == 0) {
		printf("You found a %s, but your inventory is full!\n", items[id]);
		return;
	}
	*item = malloc(sizeof(struct weapon));
	(*item)->id = id;
	printf("You found a %s! Enter a name for your item: ", items[id]);
	fgets((*item)->name, 110, stdin);
	(*item)->name[strlen((*item)->name)-1] = 0;
	if (strcmp((*item)->name, "") == 0) {
		printf("You can't quite remember what your item was or where you put it. Maybe a name would've helped?\n");
		free(*item);
		(*item)->id = 3;
	}
}

void move() {
	printf("%s", prompts[rand()%5]);
	printf(" Would you like to go north, south, east, or west?\n> ");
	char direction[10];
	fgets(direction, 10, stdin);
	if (rand() % 3 == 0) {
		if (rand() % 5 == 0) {
			fight_weeb();
		} else {
			find_item();
		}
	}
}

int main() {
	srand(time(NULL));
	gid_t gid = getegid();
	setresgid(gid, gid, gid);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	printf("Welcome to the interactive weeb hunting experience!\n");
	printf("You are kmh11, a valiant weeb hunter. You will be traversing the dangerous Otaku Forest, where weebs surround you in every direction.\n");
	initialize_weebs();
	while (1) { move(); }
}

void win() {
	system("/bin/sh");
}
