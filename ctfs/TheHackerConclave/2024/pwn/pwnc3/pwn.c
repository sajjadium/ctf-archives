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

	char name[32];
	char surname[32];

	printf("Insert your name: ");

	scanf("%s",name);

	printf("Welcome home ");
	printf(name);
	printf("\n");

	printf("Insert your first surname: ");

	scanf("%s",surname);

	printf("Insert your second surname: ");

	scanf("%s",surname);


	printf("Your user has been added!!!\n");

}

void main(){

	setbuf(stdout,0);

	pwnme();

}
