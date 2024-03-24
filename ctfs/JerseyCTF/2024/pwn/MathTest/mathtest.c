#include <stdio.h>
#include <stdlib.h>

void printflag(){
	FILE *f;
	f = fopen("flag.txt", "r");
	char flag[64];
	fread(flag, sizeof(char), 64, f);
	printf("%s\n", flag);
}

int vuln() {
	printf("Welcome to your Math Test. Perfect Score gets a Flag!\n");
	printf("Enter Name:\n");
	char name[100];
	if(scanf("%s", name) < 1){
		printf("You need a name\n");
		return 0;
	}
	long mult1 = 0x9000;
	long ans1;
	printf("%ld*x < 0. What is x\n", mult1);
       	scanf("%ld", &ans1);
	if(ans1 < 0) {
		printf("No Negatives!\n");
		return 0;
	}
	if(mult1*ans1 > 0) {
		printf("Incorrect, try again\n");
		return 0;
	}
	printf("Next Question\n");
	long mult2 = 0xdeadbeef;
	long ans2;
	printf("%ld * y = 0. What is y\n", mult2);
	scanf("%ld", &ans2);
	if(ans2 >= 0) {
                printf("Now Only Negatives!\n");
                return 0;
        }
        if((mult2*ans2) == 0) {
		printf("%ld\n", mult2*ans2);
                printf("Incorrect, try again\n");
                return 0;
        }
	printf("Final Quesiton\n");
	char mult3 = 'O';
	char ans3;
	printf("Good\n");
	printf("%c * z = 'A'. What is z?\n", mult3);
	scanf("\n%c", &ans3);
	if((char)(ans3*mult3) != 'A') {
		printf("Incorrect, try again\n");
		return 0;
	}
	printf("Final Question: ans1 + ans2 + ans3 = name\n");
	long *n = (long *)name;
	if(ans1 + ans2 + ans3 == *n) {
		printf("Congratulations! Here is your flag!!!!\n");
		printflag();
	}	
	else {
		printf("If only you had a better name :(\n");
		return 0;
	}
}

int main() {
	setvbuf(stdin, 0, _IONBF, 0);
        setvbuf(stdout, 0, _IONBF, 0);
        setvbuf(stderr, 0, _IONBF, 0);

	vuln();
}
