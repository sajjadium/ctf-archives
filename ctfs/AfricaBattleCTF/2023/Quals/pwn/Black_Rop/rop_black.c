//gcc -m32 -no-pie rop_black.c -o rop_black

#include <stdio.h>
#include <stdlib.h>


int check_file = 0;
int african = 0;
int invite_code = 0;
int capcha = 0;


void read_flag(){
	if(!(check_file && african && invite_code && capcha)) {
		printf("403|You aren't allowed to read the flag!\n");
		exit(1);
	}
	
	char flag[65];
	FILE * f = fopen("flag.txt","r");
	if (f == NULL){
		printf("flag.txt doesn't exist, try again on the server\n");
		exit(0);
	}
    fgets( flag, 65, f );
    printf("%s\n",flag);
    fflush(stdout);
}

void check_flag(char* file) {
	if(strcmp(file, "flag.txt") == 0) {
		check_file = 1;
	}
}

void check_african() {
	african = 1;
}

void check_invitecode(int code) {
	if(code == 0xbae) {
		invite_code = 1;
	}
}

void check_capcha(int login, int auth) {
	if(login == 0x062023 && auth == 0xbf1212) {
		capcha = 1;
	}
}

void vuln()
{
	char buffer[10];

	printf("check your identity and read the flag.\n");
	gets(buffer);
}

int main(){

	vuln();
}