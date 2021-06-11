#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>


void get_flag()
{
	printf("TG20{the real flag is on the server}\n");
}


void try_password()
{
	char password[20] = { 0 };
	int correct = 0;	
	printf("Please enter the password?\n");
	gets(password);
	if (correct == 1) {
		get_flag();
	} else {
		printf("Sorry, but that's not the right password...\n");
	}
	
}



int main()
{
	setvbuf(stdout, NULL, _IONBF, 0);
	try_password();
	return 0;
}
