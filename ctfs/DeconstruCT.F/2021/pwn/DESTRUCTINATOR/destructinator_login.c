#include<stdio.h>
#include<string.h>

int main(int argc,char **argv) {
	FILE *password_file;
	char password[64] = "";
	char *password_cmp = password;
	password_file = fopen("password.txt","r");
	fgets(password,sizeof(*password_file),password_file);
	fclose(password_file);
	char user_input[64] = "";
	printf("Enter password to disable destructinator:");
	fgets(user_input , sizeof(user_input), stdin);
	int eq = strncmp(user_input,password_cmp,64);
	if (eq != 0) {
		printf("Access denied\n");
		printf(user_input);
		printf("is the wrong password\n");
	}
	else {
		printf("Access Granted\nShutting down destructinator...\n");
		/* CONFIDENTIAL, code block redacted for security purposes */ 
	}
}
