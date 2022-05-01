#include <stdio.h>
#include <string.h>
#include <stdlib.h>

static void generate_name(char *str)
{
    FILE *file = fopen("/dev/urandom","r");
	fgets(str, 48, file);
	fclose(file);
}

int main(){
    char yourName[48];
    char myName[48];
    
    char guess[48];

    setbuf(stdout, NULL);

    generate_name(myName);

    printf("Hi! What's your name? ");

    int n = read(0, yourName, 48);
    if (yourName[n-1] == '\n') yourName[n-1] = '\x00';

    printf("Nice to meet you, %s!\n", yourName);

    puts("Guess my name and you'll get a flag!");

    scanf("%48s[^\n]", guess);

    if (strncmp(myName, guess, 48) == 0){
        char flag[128];

		FILE *file = fopen("flag.txt","r");
		if (!file) {
		    puts("Error: missing flag.txt.");
		    exit(1);
		}

		fgets(flag, 128, file);
		puts(flag);
    }

    puts("Bye!");
    return 0;
}