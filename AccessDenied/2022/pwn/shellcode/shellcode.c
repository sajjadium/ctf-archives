#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void main(){
	alarm(0x20);
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
	char machine_code[512];
	printf("This only understands the machine code so you have to give only the machine code, so please enter the machine code below\n");
	fgets(machine_code, 512, stdin);
	((void (*)())(machine_code))();
}