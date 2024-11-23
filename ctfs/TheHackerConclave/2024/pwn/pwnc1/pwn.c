#include <stdio.h>
#include <stdlib.h>

void print_flag(){

	FILE *f;
	char flag[128];

	if(!(f=fopen("/flag/flag.txt","r"))){

		if(!(f=fopen("./flag.txt","r"))){
			sprintf(flag,"flag{NOT_A_FLAG}");
		}else{
			fscanf(f,"%s",flag);
		}

	}else{
		fscanf(f,"%s",flag);
	}

	printf("%s\n",flag);

}

void pwnme(){

	int number;
	char name[32];

	number=0;

	printf("Insert your name: ");

	scanf("%s",name);

	printf("Welcome home %s\n",name);

	if(number == 8){

		print_flag();

	}

	exit(0);

}

void main(){

	setbuf(stdout,0);

	pwnme();

}
