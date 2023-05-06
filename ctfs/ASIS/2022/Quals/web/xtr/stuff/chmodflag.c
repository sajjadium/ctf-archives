#include <sys/stat.h>
#include <stdio.h>

int main(){
	chmod("/flag.txt",0444);
	perror("status");
}