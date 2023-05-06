#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int initialized = 0;
char editbuf[0x100];

int menu(){
	puts("Your options are:");
	puts("1) Edit Position");
	puts("2) Display string");
	puts("3) Exit program\n");
	puts("What would you like to do?");

	int ret;
	scanf("%d", &ret);
	
	puts("");
	return ret;
}

void edit(){
	puts("Great! Please input the index you'd like to change!");
	
	int index;
	scanf("%d", &index);
	getchar();

	puts("Nice!, Now select the character you'd like to change it to!");
	scanf("%c", &editbuf[index]);
	puts("");	
}

int main(){
	setbuf(stdout, 0x0);
	setbuf(stderr, 0x0);

	puts("Welcome to the string editor!\n");

	char buf[0x80];
	if(!initialized){
		puts("Please input your initial string (don't worry, we do not use gets):");

		read(0x0, buf, 0xb0);

		initialized = 1;
	}else{
		puts("Um... that's strange.");
	}

	puts("");

	puts("Great! Now, you can begin editing your string!\n");

	while(1){
		int choice = menu();
		if(choice == 1){
			strcpy(editbuf, buf);
			edit();
			strcpy(buf, editbuf);
		}else if(choice == 2){
			puts("Great! Here's your string:");
			printf("%s\n", buf);
		}else{
			puts("Great! Hope you accomplished what you wanted!");
			break;
		}
	}

	return 0;
}
