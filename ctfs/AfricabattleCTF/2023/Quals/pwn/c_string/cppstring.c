#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void init()
{
	setbuf(stdin, 0);
	setbuf(stdout, 0);
	setbuf(stderr, 0);
}

void getsline(char **p, size_t *n)
{
	char c = '\0';
	unsigned int count = 0, size = 0;
	char *backup;

	if (*n==0 && *p==NULL)
	{
		*p = malloc(0);
		while (1)
		{
			read(0, &c, 1);
			if (count >= 0x20000)
				exit(0);
			if (count != 0 && count % 0x10 == 0)
			{
				backup = malloc(count + 0x10);
				memcpy(backup, *p, count);
				*p = backup;
			}
			backup = *p;
			backup[count] = c;

			count++;
			if (c=='\n')
			{
				*n = count;
				break;
			}
		}
	}
	else
		read(0, p, *n);

}

void cin(char **p)
{
	size_t n = 0;
	char *buffer = NULL;

	// memset(*p, 0, 0x400);
	getsline(&buffer, &n);
	if (strlen(buffer) > 0x408)
		*p = buffer;
	else
		memcpy(*p, buffer, n);
}

void cout(char *p)
{
	unsigned int count = 0;
	while (1)
	{
		if (p[count]=='\0')
			break;
		write(1, &p[count], 1);
		count++;
	}
}

/*
Challenge name: C++ string
*/

unsigned long int gen_seed()
{
	return ((time(0)*2003/1/9) >> 2) * (rand()*0x09012021/5);
}

void play_game()
{
	unsigned long int randnum, guess;
	char *p;
	char buffer[0x408];

	randnum = rand();

	cout("------ GUESSING GAME ------\n");
	cout("Rule: You will guess a number from 0 to 4294967295 and if you win, I will give you a gift!\n");
	cout("Your number: ");

	p = buffer;
	cin(&p);
	cout("You guess: ");
	cout(p);
	guess = atoi(p);
	sleep((rand() % 5) + 1);

	if (randnum == guess)
	{
		cout("Congratulation! Name for the winner: ");
		p = buffer;
		cin(&p);
		cout("You can get the gift from admin, ");
		cout(p);
	}
	else
	{
		cout("Nah loser!\n");
		exit(0);
	}
}

int main()
{

	init();
	srand(gen_seed());
	srand(gen_seed());
	srand(gen_seed());

	play_game();
}