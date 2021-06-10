#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<fcntl.h>
#include<unistd.h>

#define HK 0x1337

char *note[0x2];

long int getnum()
{
	char buffer[0x20];
	read(0,buffer,0x18);
	return atoll(buffer);
}
void setup()
{
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	setvbuf(stderr,0,2,0);
	alarm(20);
}

void handler()
{
	char buffer[0x100];
	long int idx;
	note[0] = (char *)malloc(0x200);
	note[1] = (char *)malloc(0x200);
	printf("I need your name: ");
	read(0,buffer,0x50);
	puts(buffer);
	printf("Enter the index of the you want to write: ");
	idx = getnum();
	if(idx < 2) {
		printf("Enter data: ");
		read(0,note[idx],0xe8);
	}
	puts("Bye");
	_exit(HK);
}
int main()
{
	setup();
	handler();
	return 0;
}
