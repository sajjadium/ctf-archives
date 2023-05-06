

#include<stdio.h>
#include<stdlib.h>

struct meme
{
	void (*func)(char*);
	char* content;
};


struct meme** memes;


void init()	{
	setvbuf(stdout, NULL, _IONBF, 0);
	memes = malloc(8 * sizeof(void *));
}

unsigned int read_int()	{
	char buf[16];
	fgets(buf, 16, stdin);
	return strtoul(buf, NULL, 10);
}

void print_menu()	{
	puts("===Meme Creator===");
	puts("1. New Meme");
	puts("2. Edit Meme");
	puts("3. Print Meme");
	puts("4. Exit");
	puts("==================");
	printf("Choice: ");
}

void EZ_WIN()	{
	puts("EAAAAAAAAAAAASYYYYYYYYYYYYY");
	system("/bin/sh");
	exit(0);
}

void my_print(char* buf)	{
	printf("Content: %s\n", buf);
}

void new_meme()	{
	unsigned int size;
	printf("Enter meme size: ");
	size = read_int();
	if(size > 0x200)	{
		puts("Please, noone wants to read the entire bee movie script");
		exit(-1);
	}
	int i = 0;
	while(memes[i] != NULL && ++i < 8);
	if(i == 8)	{
		puts("No more memes for you!");
		exit(-1);
	}
	memes[i] = malloc(8);
	memes[i]->func = &my_print;
	memes[i]->content = malloc(size);
	printf("Enter meme content: ");
	fgets(memes[i]->content, size, stdin);
	puts("Done!");
}

void edit_meme()	{
	unsigned int idx;
	printf("Index: ");
	idx = read_int();
	if(memes[idx] == NULL)	{
		puts("There's no meme there!");
		return;
	}
	printf("Enter meme content: ");
	gets(memes[idx]->content);
	puts("Done!");
}

void print_meme()	{
	unsigned int idx;
	printf("Index: ");
	idx = read_int();
	if(memes[idx] == NULL)	{
		puts("There's no meme there!");
		return;
	}
	(*(memes[idx]->func))(memes[idx]->content);
}

int main(int argc, char const *argv[])
{
	unsigned int choice;

	init();
	while(1)	{
		print_menu();
		choice = read_int();
		switch(choice)	{
			case 1:
				new_meme();
				break;
			case 2:
				edit_meme();
				break;
			case 3:
				print_meme();
				break;	
			case 4:
				puts("Bye bye!");
				exit(0);
				break;
			default:
				puts("Invalid choice!");
				break;
		}
	}
	return 0;
}