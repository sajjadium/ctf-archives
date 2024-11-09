#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>

int guess = 1;

struct Node {
	void (*func_ptr) ();
	struct Node *next;
};

void win()
{
	char flag_buf[64];
	FILE *fp = fopen("flag.txt", "r");
	fgets(flag_buf, 64, fp);
	printf("%s", flag_buf);
	fclose(fp);
}

void add()
{
	guess += 3;
}

void mul()
{
	guess *= 3;
}

struct Node *history_travel(struct Node *history)
{
	if (history->next == NULL)
	{
		return history;
	}
	else
	{
		return history_travel(history->next);
	}
}

struct Node *history_add(struct Node *history, 	void (*f)())
{
	struct Node *new = malloc(sizeof(struct Node));
	new->next = NULL;
	new->func_ptr = f;

	if (history == NULL)
	{
		return new;
	}
	else
	{
		struct Node *last = history_travel(history);
		last->next = new;
		return history;
	}
}

void history_repeat(struct Node *history)
{
	if (!history->func_ptr)
	{
		return;
	}
	history->func_ptr();
	printf("Guess is %d\n", guess);
	if (history->next == NULL)
	{
		return;
	}
	else
	{
		return history_repeat(history->next);
	}
}

void history_pop(struct Node *history)
{
	struct Node *last_node = history_travel(history);
	free(last_node);
	last_node->next = NULL;
	last_node->func_ptr = NULL;
}

void leetify(char *buffer)
{
	for (int i = 0; buffer[i] != '\0'; i++)
	{
		switch (buffer[i])
		{
			case 'o':
				buffer[i] = '0';
				break;
			case 'S':
			case 's':
				buffer[i] = '5';
				break;
			case 'a':
			case 'A':
				buffer[i] = '4';
				break;
			case 'i':
			case 'I':
				buffer[i] = '1';
				break;
			case 'e':
			case 'E':
				buffer[i] = '3';
				break;
		}
	}
}

int main()
{
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);

	srand(time(NULL));
	int secret = rand() % 1000;

	char buffer[64];
	printf("Enter your name: ");
	fgets(buffer, 64, stdin);

	void (*win_ptr) () = &win;
	void (*add_ptr) () = &add;
	void (*mul_ptr) () = &mul;

	leetify(buffer);

	printf("Welcome to Game of Three, ");
	printf(buffer);
	printf("Your guess starts with 1. You can add (+) or multiply (*) your guess by three.\nThe game will tell you if you are higher or lower that the secret.\nYou can delete your last move with 'd'. You cannot make any new moves after deleting.\nYou can replay all your moves by pressing 'r'\nFinally, make a guess by pressing 'g'\n\n");

	char input;
	char *message;
	struct Node *history;
	bool run = true;

	int once = 1;
	while (run)
	{
		if (guess > secret)
			printf("%d is greater than secret\n", guess);
		else
			printf("%d is less than secret\n", guess);
		
		printf("Input: ");
		input = fgetc(stdin);
		fgetc(stdin); // eat the newline
		switch (input)
		{
			case '+':
				if (once)
				{
					history = history_add(history, add_ptr);
					add();
				}
				else
					puts("Cant do that anymore");
				break;
			case '*':
				if (once)
				{
					history = history_add(history, mul_ptr);
					mul();
				}
				else
					puts("Cant do that anymore");
				break;
			case 'r':
				guess = 1;
				printf("---REPLAY---\n");
				history_repeat(history);
				printf("------------\n");
				break;
			case 'q':
				puts("Exiting!");
				run = false;
				break;
			case 'd':
				if (once)
				{
					history_pop(history);
					once = 0;
					puts("Previous entry has been deleted");

					guess = 1;
					printf("---REPLAY---\n");
					history_repeat(history);
					printf("------------\n");
				}
				else
				{
					puts("You can do that only once!");
				}
				break;
			case 'e':
				puts("TODO: Leave a message for the creator!");
				message = malloc(sizeof(struct Node));
				read(0, message, sizeof(struct Node));
				break;
			case 'g':
				printf("You were %d away from secret\n", guess - secret);
				run = false;
				break;
			default:
				printf("Invalid operation\n");
				break;
		}
	}
}
