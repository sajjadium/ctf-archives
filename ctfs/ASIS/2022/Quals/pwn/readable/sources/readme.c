#include <stdio.h>
#include <unistd.h>

const char *flag = "ASIS{test-flag}"; 

int main(){
	flag = "No flag for you";
	puts(flag);
	return 0;
}