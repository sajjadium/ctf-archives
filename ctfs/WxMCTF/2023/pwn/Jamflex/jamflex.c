#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>

int val(char* pw, int len){
	int out = 0;
	for(int i = 0 ; i < len; i++){
		out += pw[i];
	}
	return out;
}

void main(){
	setvbuf(stdin, NULL, 2, 0);
    setvbuf(stdout, NULL, 2, 0);
	char username[25];
	int fd;
	if(fd = open("~/password.txt", O_RDONLY,0400) > 0){
		printf("Password file couldn't be found.\n");
		return;
	}
	char pw1[10];
	int length;
	if(!(length = read(fd,pw1,10) > 0)){
		printf("Password file couldn't be read.\n");
		close(fd);
		return;
	}
	printf("jamflex login system\n");
	printf("username: ");
	scanf("%5s", &username);
	int pw2;
	printf("password: ");
	scanf("%d", &pw2);
	int value = val(pw1,10);
	if(value == pw2){
		printf("my bank pin is 1234 btw\n");
		system("cat ./flag.txt");
	}
	else printf("lmfao you noob try again");
	printf("\n");
}
