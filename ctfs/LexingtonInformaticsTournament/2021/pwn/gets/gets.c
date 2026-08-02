#include <stdio.h>
#include <stdlib.h>

int main(){
	setbuf(stdout, 0x0);
	setbuf(stderr, 0x0);

	puts("Gets is very secure. You may see other sources tell you otherwise, but they are wrong.");
	puts("Geeksforgeeks says gets is insecure. G4g also says graph coloring can be solved in O(n).");
	puts("Wikipedia says gets is insecure. Anyone can write anything on wikipedia, it is unreliable.");
	puts("The linux docs say gets is insecure. No one reads the linux docs except stuck up nerds.");
	puts("My compiler warned me gets is insecure. My compiler also can't add semicolons automatically");
	puts("Hopefully you can see that gets is in fact secure, and all who tell you otherwise are lying.\n");

	puts("Are you starting to understand?");

	long debug = 0;
	char buf[0x20];
	gets(buf);

	if(strcmp(buf, "Yes") == 0){
		puts("I'm glad you understand.");
		if(debug == 0xdeadbeef){
			FILE *f = fopen("flag.txt","r");
			if(f == NULL){
				puts("Something is wrong. Please contact Rythm.");
				exit(1);
			}

			fgets(buf, 0x20, f);

			puts("Debug info:");
			puts(buf);
		}
	}else{
		puts("Think Mark, think! Gets is secure!");
	}

	return 0;
}
