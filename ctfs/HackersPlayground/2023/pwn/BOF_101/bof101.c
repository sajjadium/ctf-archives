#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

void printflag(){ 
	char buf[32];
	int fd = open("/flag", O_RDONLY);
	read(fd, buf, sizeof(buf));
	close(fd);
	puts(buf);
}

int main() {
	int check=0xdeadbeef;
	char name[140];
	printf("printflag()'s addr: %p\n", &printflag);
	printf("What is your name?\n: ");
	scanf("%s", name);	
	if (check != 0xdeadbeef){
		printf("[Warning!] BOF detected!\n");
		exit(0);
	}
	return 0;
}
