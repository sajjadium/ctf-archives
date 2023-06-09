#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


extern void *xmalloc(size_t size);
extern void xfree(void *ptr);	

void *chunks[0x20] = {};

typedef unsigned long long int u64;
typedef unsigned int u32;

void init() 
{
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	alarm(60);
}

u32 read_int() {
	char buf[8];
	if (fgets(&buf, 8, stdin) == NULL) exit(0);
	buf[strlen(&buf) - 1] = 0;
	return (u32)strtol(&buf, NULL, 10);
}

u32 get_next_chunk_index() {
	for (u32 i = 0; i < 0x20; i++) {
		if (chunks[i] == NULL) return i;
	}
	return -1;
}

void alloc() {
	u32 size;
	printf("Size: ");
	size = read_int();

	if (size <= 0x4000) {
		u32 index = get_next_chunk_index();
		if (index < 0x20) {
			printf("Index: %u\n", index);
		} else {
			puts("No more allocations");
			return;
		}
		void *data = xmalloc(size);
		if (data != NULL) {
			chunks[index] = data;
		} else {
			puts("Alloc failed");
		}
	} else {
		puts("Allocation is to big");
	}
		
}

void delete() {
	u32 index;
	printf("Index: ");
	index = read_int();
	if (index < 0x20 && chunks[index] != NULL) {
		xfree(chunks[index]);
		chunks[index] = NULL;
	} else {
		puts("Invalid index");
	}
}

void edit() {
	u32 index;
	printf("Index: ");
	index = read_int();
	if (index < 0x20 && chunks[index] != NULL) {
		printf("Data: ");
		// I left this overflow for you. There's no way to do anything with it anyways,
		// because the heap security is to good.
		read(0, chunks[index], 0x1000);
	} else {
		puts("Invalid index");
	}
}

void show() {
	u32 index;
	printf("Index: ");
	index = read_int();
	if (index < 0x20 && chunks[index] != NULL) {
		puts(chunks[index]);
	} else {
		puts("Invalid index");
	}
}

void menu() {
	puts("==========SecureHeap Sandbox==========");
	puts("\t[1] Alloc");
	puts("\t[2] Free");
	puts("\t[3] Edit");
	puts("\t[4] Show");
	puts("\t[0] Exit");
	printf("> ");
}

int main() 
{
	init();
	u32 choice;
	while (1) {
		menu();
		choice = read_int();
		if (choice == 1) {
			alloc();
		} else if (choice == 2) {
			delete();
		} else if (choice == 3) {
			edit();
		} else if (choice == 4) {
			show();
		} else {
			break;
		}
	}
	return 0;
}