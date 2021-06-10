#include <stdio.h>
//#include <fcntl.h>
//#include <unistd.h>
#include <stdlib.h>
#include <string.h>

void printflag(){ 
	char buf[32];
	FILE* fp = fopen("/flag", "r"); 
	fread(buf, 1, 32, fp);
	fclose(fp);
	printf("%s", buf);
	fflush(stdout);
}

int main() {
	int check=0xdeadbeef;
	char name[140];
	printf("printflag()'s addr: %p\n", &printflag);
	printf("What is your name?\n: ");
	fflush(stdout);
	scanf("%s", name);	
	if (check != 0xdeadbeef){
		printf("[Warning!] BOF detected!\n");
		fflush(stdout);
		exit(0);
	}
	return 0;
}
