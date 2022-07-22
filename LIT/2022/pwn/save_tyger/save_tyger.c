#include <stdlib.h>
#include <stdio.h>

char flag[64];

int main(){
	long pass;
	char buf[32];
	pass = 0;
	printf("Oh no, someone stole our one and only Tyger! :noo:\n");
	printf("Would you help us save him?\n");
	gets(buf);
	if(pass == 0xabadaaab){
		printf("It worked!\n");
		FILE *f = fopen("flag.txt", "r");
		if(f == NULL){
			printf("Something went wrong. Please let Eggag know.\n");
			exit(1);
		}
		fgets(flag, 64, f);
		puts(flag);
	}
	else printf("WE NEED HIM BAAACK!\n");
}