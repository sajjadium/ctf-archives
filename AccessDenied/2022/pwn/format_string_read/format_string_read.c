#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char flag[64];

void main(){
	char name[32];
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    alarm(0x20);
	FILE *f = fopen("flag.txt","r");
	if (f == NULL) {
		printf("Flag File is Missing. \n");
		exit(0);
	}
	fgets(flag, 64,f);
	puts("Enter your name");
	read(0, name, 32);
	printf(name);
}