#include <stdio.h>
#include <unistd.h>

int main(){
	long pass;
	puts("Welcome to battleCTF Event portal.");
	printf("Enter you invite code to participe:");
	scanf("%s",&pass);
	if(pass * 0x726176656e70776eu == 0x407045989b3284aeu){
		execl("/bin/sh", "sh", 0);
	}
	else
		puts("\nWrong password ..!");
	return 0;
}

