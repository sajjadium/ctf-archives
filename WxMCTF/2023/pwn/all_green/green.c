#include <stdio.h>
#include <stdlib.h>
int one = 0;
int two = 0;
int three = 0;

void check1(int in){
	one = in;
}

void check2(int in){
	two = in;
}

void check3(int in){
	three = in;
}

void finalcheck(int in){
	if(one == 0x1337 && two == 0x420 && three == 0xDEADBEEF && in == 0x123){
		const char* flag = getenv("FLAG");
        if(flag == NULL) {
    	    printf("Flag not found!");
    	    exit(0);
        }
        printf("%s\n",flag);
	}
}

void func(){
    printf("Every protection is enabled. Good luck.\n");
    char buf[0x20];
    gets(buf);
    printf(buf);
    printf("\n");
    gets(buf);
}

int main() {
    setvbuf(stdin, NULL, 2, 0);
    setvbuf(stdout, NULL, 2, 0);
    func();
}
