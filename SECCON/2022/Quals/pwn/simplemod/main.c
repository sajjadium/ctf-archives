#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int getint(void);
void modify(void);
__attribute__((noreturn)) void exit_imm(int status);

__attribute__((constructor))
static int init(){
	alarm(30);
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	return 0;
}

__attribute__((destructor))
static void fini(){
	exit_imm(0);
}

static int menu(void){
	puts("\nMENU\n"
			"1. Modify\n"
			"0. Exit\n"
			"> ");

	return getint();
}

int main(void){
	puts("You can operate 30 times.");
	for(int i=0; i<30; i++){
		switch(menu()){
			case 0:
				goto end;
			case 1:
				modify();
				puts("Done.");
				break;
		}
	}

end:
	puts("Bye.");
	return 0;
}
