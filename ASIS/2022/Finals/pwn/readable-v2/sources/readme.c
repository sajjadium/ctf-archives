#include <stdio.h>
#include <unistd.h>

const char *flag = "ASIS{test-flag}"; 

int main(int argc){
	flag = "No flag for you";
	puts(flag);
	return 0;
}