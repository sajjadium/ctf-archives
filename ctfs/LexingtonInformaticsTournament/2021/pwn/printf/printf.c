#include <stdio.h>
#include <stdlib.h>

int main(){
	setbuf(stdout, 0x0);
	setbuf(stderr, 0x0);

	FILE *f = fopen("flag.txt", "r");
	if(f == NULL){
		puts("Something is wrong. Please contact Rythm.");
		exit(1);
	}	

	char *buf = malloc(0x20);
	char *flag = malloc(0x20);
	fgets(flag, 0x20, f);

	puts("Maybe gets isn't secure? Well, at least no where seems to warn printf is insecure. Right?");

	scanf("%20s", buf);

	printf(buf);

	puts("\nGlad we have come to agreement!");

	free(buf);
	free(flag);

	return 0;
}

