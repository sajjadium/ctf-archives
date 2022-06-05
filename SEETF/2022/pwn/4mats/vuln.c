#include <stdio.h>
#include <stdlib.h>
#include <time.h>

char name[16];
char echo[100];
int number;
int guess;
int set = 0;
char format[64] = {0};


void guess_me(int fav_num){
    printf("Guess my favourite number!\n");
    scanf("%d", &guess);
    if (guess == fav_num){
        printf("Yes! You know me so well!\n");
	system("cat flag");
        exit(0);}
   else{
       printf("Not even close!\n");
   }
       
}


int main() {

mat1:
    printf("Welcome to SEETF!\n");
    printf("Please enter your name to register: %s\n", name);
    read(0, name, 16);

    printf("Welcome: %s\n", name);

    while(1) {
mat2:
        printf("Let's get to know each other!\n");
        printf("1. Do you know me?\n");
        printf("2. Do I know you?\n");

mat3:
        scanf("%d", &number);


        switch (number)
        {
            case 1:
                srand(time(NULL));
                int fav_num = rand() % 1000000;
		set += 1;
mat4:
                guess_me(fav_num);
                break;

            case 2:
mat5:
                printf("Whats your favourite format of CTFs?\n");
		read(0, format, 64);
                printf("Same! I love \n");
		printf(format);
                printf("too!\n");
                break;

            default:
                printf("I print instructions 4 what\n");
		if (set == 1)
mat6:
                    goto mat1;
		else if (set == 2)
		    goto mat2;
		else if (set == 3)
mat7:
                    goto mat3;
		else if (set == 4)
                    goto mat4;
		else if (set == 5)
                    goto mat5;
		else if (set == 6)
                    goto mat6;
		else if (set == 7)
                    goto mat7;
                break;
        }
    }
    return 0;
}
