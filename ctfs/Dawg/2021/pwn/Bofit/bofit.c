#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <unistd.h>

void win_game(){
	char buf[100];
	FILE* fptr = fopen("flag.txt", "r");
	fgets(buf, 100, fptr);
	printf("%s", buf);
}

int play_game(){
	char c;
	char input[20];
	int choice;
	bool correct = true;
	int score = 0;
	srand(time(0));
	while(correct){
		choice = rand() % 4;
		switch(choice){
			case 0:
				printf("BOF it!\n");
				c = getchar();
				if(c != 'B') correct = false;
				while((c = getchar()) != '\n' && c != EOF);
				break;

			case 1:
				printf("Pull it!\n");
				c = getchar();
				if(c != 'P') correct = false;
				while((c = getchar()) != '\n' && c != EOF);
				break;

			case 2:
				printf("Twist it!\n");
				c = getchar();
				if(c != 'T') correct = false;
				while((c = getchar()) != '\n' && c != EOF);
				break;

			case 3:
				printf("Shout it!\n");
				gets(input);
				if(strlen(input) < 10) correct = false;
				break;
		}
		score++;
	}
	return score;
}

void welcome(){
	char input;
	printf("Welcome to BOF it! The game featuring 4 hilarious commands to keep players on their toes\n");
	printf("You'll have a second to respond to a series of commands\n");
	printf("BOF it: Reply with a capital \'B\'\n");
	printf("Pull it: Reply with a capital \'P\'\n");
	printf("Twist it: Reply with a capital \'T\'\n");
	printf("Shout it: Reply with a string of at least 10 characters\n");
	printf("BOF it to start!\n");
	input = getchar();
	while(input != 'B'){
		printf("BOF it to start!\n");
		input = getchar();
	}
	while((input = getchar()) != '\n' && input != EOF);
}

int main(){
	int score = 0;
	welcome();
	score = play_game();
	printf("Congrats! Final score: %d\n", score);
	return 0;
}
