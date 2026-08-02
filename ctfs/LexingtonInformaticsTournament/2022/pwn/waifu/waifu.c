#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
	setbuf(stdout, 0x0);

	FILE *f = fopen("flag.txt", "r");
	if(f == NULL){
		puts("Something is wrong. Please contact Rythm.");
		exit(1);
	}	

	char *buf = malloc(0x20);
	char *flag = alloca(0x1000);
	fgets(flag, 0x1000, f);

	puts("Do you like waifus?");

	scanf("%20s", buf);
	puts("");

	if(!strcmp(buf, "yes")){
		puts("Good.");
	}else{
		puts("Wtmoo how could you say:");
		printf(buf);
		puts("");
	}

	free(buf);

	return 0;
}
