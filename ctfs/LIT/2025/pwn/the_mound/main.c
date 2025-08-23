#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

#define SIZE 0x10000

typedef struct _Rock {
	unsigned int len;
	char content[];
} Rock;

typedef struct _Mound {
	unsigned int reach;
	Rock *list[64];
} Mound;

Mound *mound;

int prompt() {
	printf(">  ");
}

Rock *create(unsigned int size) {
	if (size >= 0x400) {
		puts("Size too large");
		clean();
	}
	unsigned int rockSize = size/16;
	rockSize *= 16;
	rockSize += 16;
	unsigned int idx = rockSize / 16;
	
	Rock *available = mound->list[idx];
	if (available != NULL) {
		Rock *ret = available;
		ret->len = size;
		
		memcpy(&mound->list[idx], available->content, 8);
		memset(ret->content, 0, rockSize);
		return ret;
	}
	else {
		Rock *ret = (Rock *) ((char *) mound + mound->reach);
		ret->len = size;
		mound->reach += rockSize + sizeof(ret->len);
		if (mound->reach >= SIZE - rockSize - sizeof(ret->len)) {
			puts("Memory error");
			clean();
		}
		memset(ret->content, 0, rockSize);
		return ret;
	}
}

int del(Rock *rock) {
	int size = rock->len;
	unsigned int rockSize = size/16;
	rockSize *= 16;
	rockSize += 16;
	unsigned int idx = rockSize / 16;
	memcpy(rock->content, &mound->list[idx], 8);
	mound->list[idx] = rock;
	return 0;
}

int menu() {
	puts("1. Create a rock");
	puts("2. Delete a rock");
	puts("3. View rock contents");
	puts("4. Edit rock");
	puts("0. Exit");
	prompt();
	return 0;
}

int init() {
	mound = (Mound *) mmap(0, SIZE, PROT_READ | PROT_WRITE, MAP_ANON | MAP_PRIVATE, -1, 0);
	mound->reach = sizeof(mound->reach) + sizeof(mound->list);
}

int clean() {
	munmap(mound, SIZE);
	exit(0);
}

Rock *rocks[16];

unsigned int getIdx() {
	unsigned int idx;
	puts("Idx?");
	prompt();
	scanf("%u%*c", &idx);
	if (idx >= 16) {
		puts("Invalid idx");
		clean();
	}
	if (rocks[idx] == NULL) {
		puts("No rock located at this index");
		clean();
	}
	return idx;
}

int main() {
	setbuf(stdout, 0);
	setbuf(stderr, 0);
	init();
	while (1) {
		menu();
		char op = getchar();
		getchar();
		
		switch (op) {
			case '0':
				clean();
				break;
			case '1': {
				unsigned int size;
				unsigned int idx;
				puts("Idx?");
				prompt();
				scanf("%u%*c", &idx);
				if (idx >= 16) {
					puts("Invalid idx");
					clean();
				}
				if (rocks[idx] != NULL) {
					puts("Rock at this index already exists.");
					clean();
				}
				puts("Size?");
				prompt();
				scanf("%u%*c", &size);
				rocks[idx] = create(size);
				puts("Rock created");
				break;
			}
			case '2': {
				unsigned int idx = getIdx();
				del(rocks[idx]);
				rocks[idx] = 0;
				puts("Rock deleted");
				break;
			}
			case '3': {
				unsigned int idx = getIdx();
				printf("Rock content: %s\n", rocks[idx]->content);
				break;
			}
			case '4': {
				unsigned int idx = getIdx();
				puts("Content?");
				unsigned int len = rocks[idx]->len;
				//rocks[idx]->content
				prompt();
				rocks[idx]->content[read(0, rocks[idx]->content, len) - 1] = 0;
				puts("Rock edited successfully");
				break;
			}
		}
	}
	return 0;
}
