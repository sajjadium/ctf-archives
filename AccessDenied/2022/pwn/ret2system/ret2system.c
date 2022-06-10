#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
char store[64];

void vuln(){
	char buf[32];
	system("date");
	printf("You are allowed to store some value\n");
	fgets(store, 64, stdin);
	printf("Enter the buffer now\n");
	fgets(buf, 64, stdin);
}

void main(){
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    alarm(0x20);
    vuln();
}