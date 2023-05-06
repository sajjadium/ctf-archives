#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<string.h>

void initialize()
{
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	setvbuf(stderr,0,2,0);
	alarm(30);
}

int main()
{
	char buf[0x20];
	int sum = 0;
	initialize();
	puts("Memory leak detected:");
	printf("%p\n",&buf);
	puts("Enter your code of action:");
	read(0,buf,0x50);
	return 0;
}
