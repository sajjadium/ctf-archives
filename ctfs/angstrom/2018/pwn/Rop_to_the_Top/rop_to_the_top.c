
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

void the_top(){

	system("/bin/cat flag");

}

void fun_copy(char *input){

	char destination[32];
	strcpy(destination, input);
	puts("Done!");
}

int main (int argc, char **argv){
	gid_t gid = getegid();
	setresgid(gid,gid,gid);

	if (argc == 2){
		puts("Now copying input...");
		fun_copy(argv[1]);
	} else {
		puts("Usage: ./rop_to_the_top32 <inputString>");
	}

	return 0;
}
