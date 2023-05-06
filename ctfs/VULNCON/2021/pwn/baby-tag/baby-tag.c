// gcc -no-pie -o baby-tag baby-tag.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define SIZE 0x60
char * chunk = NULL;
unsigned long tag = 0;
long allowed_access = 1;

void welcome()
{
	alarm(0x60);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	tag = (unsigned long)malloc(SIZE);
	free((char *)tag);
	tag = tag >> 12;
}

unsigned long menu()
{
	unsigned long choice = 0;
	printf("1. Allocate\n2. Delete\n3. Edit\n> ");
	scanf("%lu", &choice);
	return choice;
}

void allocate()
{
	if (allowed_access != 1)	return;

	chunk = (char *)malloc(SIZE);

	if (((long)chunk >> 12) ^ tag)
	{
		puts("[+]Hacker detected.");
		puts("[!]Condition zero active.");
		allowed_access = 0;
		return;
	}
	if (!chunk)	return;

	printf("Contents> ");
	unsigned long n = read(0, chunk, SIZE-1);

	chunk[n] = '\0';
}

void delete()
{
	if (allowed_access != 1)	return;
	if (!chunk)	return;

	free(chunk);
}

void edit()
{
	if (!chunk)	return;

	printf("Contents> ");
	unsigned long n = read(0, chunk, SIZE-1);
	chunk[n] = '\0';

	printf("You just entered: ");
	puts(chunk);
}

int main()
{
	welcome();
	while(1)
	{
		switch(menu())
		{
			case 1:
				allocate();
				break;

			case 2:
				delete();
				break;
			
			case 3:
				edit();
				break;

			default:
				puts("Bye.");
				return 0;
		}
	}
}