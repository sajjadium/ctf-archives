#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void flag_me(){
	system("cat flag.txt");
}

void lockdown(){
	int lock = 0;
	char buf[64];
	printf("I made this really cool flag but Governor Hogan put it on lockdown\n");
	printf("Can you convince him to give it to you?\n");
	gets(buf);
	if(lock == 0xdeadbabe){
		flag_me();
	}else{
		printf("I am no longer asking. Give me the flag!\n");
	}
}

int main(){
	lockdown();
	return 0;
}
