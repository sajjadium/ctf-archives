#include <stdlib.h>
#include <stdio.h>

void cell(){
	printf("Thank god you got him out of this cockroach-infested cell!\n");
	FILE *f = fopen("flag.txt", "r");
	char flag[64];
	if(f == NULL){
		printf("Something went wrong. Please let Eggag know.\n");
		exit(1);
	}
	fgets(flag, 64, f);
	puts(flag);
    exit(0);
}

int main(){
	char buf[32];
	printf("NOOOO, THEY TOOK HIM AGAIN!\n");
	printf("Please help us get him out or there is no way we will be able to prepare LIT :sadness:\n");
	gets(buf);
}
