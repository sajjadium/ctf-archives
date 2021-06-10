#include <stdbool.h> 
#include<stdio.h>
#include<stdlib.h>

void win(long long p1, long long p2)	{
	FILE* fp;
	char* buf = malloc(100);
	if(p1 == 0xbeefdeaddeadbeef)
		fp = fopen("flag.txt", "r");
	if(p2 == 0xdeadbeefbeefdead)	{
		fgets(buf, 100, fp);
		puts(buf);
	}
}

void vuln()	{
	char buf[8];
	gets(buf);
}

void check(char i[], char j[], int *x, FILE *fp)	{
        FILE* my_file;
	char c;
	printf("Answer = ");
	fgets(i, 10, stdin);
	fgets(j, 10, fp);
	if (strcmp(i, j) == 0)	{
		puts("Correct!");
		*x += 1;
	}
	else	{
		puts("Wrong!");
	}
}

int main(int argc, char const *argv[])
{
	setvbuf(stdout, NULL, _IONBF, 0);
	char ans1[10];
	char ans2[10];
	char temp[100];
	bool a = true;
	int x = 1;
	
	printf("Welcome to sudoku game, player!");
	printf("This game has 3 different levels. Each level has 3 diffrent sudoku puzzles\n");
	printf("Level 1: Normal sudoku\n");
	printf("Level 2: Diagonal sudoku\n");
	printf("Level 3: Diagonal with anti-knight move sudoku\n");
	printf("To answer the questions, you have to write the true numbers of A-H\n");
	printf("Ex: Answer = 12345678\n");
	printf("\n");

	FILE *fp;

	while (a)	{
		if (x < 3)	{
			fp = popen("python generate1.py", "r");
			if (fp == NULL) {
				printf("Error\n" );
				exit(1);
			}
			for(int i = 0; i < 13; i++)	{
				printf("%s", fgets(temp, 100, fp));
			}
			check(ans1, ans2, &x, fp);
			pclose(fp);
		}
		else if (x < 6)	{
			fp = popen("python generate2.py", "r");
			if (fp == NULL) {
				printf("Error\n" );
				exit(1);
			}
			for(int i = 0; i < 13; i++)	{
				printf("%s", fgets(temp, 100, fp));
			}
			check(ans1, ans2, &x, fp);
			pclose(fp);
		}
		else if (x < 9)	{
			fp = popen("python generate3.py", "r");
			if (fp == NULL) {
				printf("Error\n" );
				exit(1);
			}
			for(int i = 0; i < 13; i++)	{
				printf("%s", fgets(temp, 100, fp));
			}
			check(ans1, ans2, &x, fp);
			pclose(fp);
		}
		else {
			a = false;
		}
	}
	
	puts("Welcome to ROP 64 bit!");	
	vuln();			
	
	return 0;
}
