#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


char *flag = "REDACTED";
char buf[50];

int main(int argc, char **argv) {

	
	puts("Welcome to the number guessing game!");
	puts("Before we begin, please enter your name (40 chars max): ");
	fflush(stdout);
	fgets(buf, 40, stdin);
	buf[strlen(buf)-1] = '\0';
		
	strcat(buf, "'s guess: ");	
	puts("I'm thinking of two random numbers (0 to 1000000), can you tell me their sum?");
	
	srand(time(NULL));
	int rand1 = rand() % 1000000;
	int rand2 = rand() % 1000000;

	printf(buf);
	fflush(stdout);
	int guess;
	char num[8];
	fgets(num,8,stdin);
	sscanf(num,"%d",&guess);

	if (guess == rand1+rand2){
		printf("Congrats, here's a flag: %s\n", flag);
	} else {
		printf("Sorry, the answer was %d. Try again :(\n", rand1+rand2); 
	}
	fflush(stdout);
	return 0;
}

