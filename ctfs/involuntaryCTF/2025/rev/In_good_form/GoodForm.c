#include <stdio.h>
#include <string.h>

int main() 
{
    char flag[64];

    char username[256];
    char password[256];

    char inputUsername[256];
    char inputPassword[256];

    //Read files
    FILE *fd1 = fopen("/var/app/current/challenges/Reverse\ engineering/In\ good\ form/username.txt", "r");
    fgets(username, 256, fd1);
    fflush(stdout);

    FILE *fd2 = fopen("/var/app/current/challenges/Reverse\ engineering/In\ good\ form/password.txt", "r");
    fgets(password, 256, fd2);
    fflush(stdout);   


    printf("Admin login\n");

    printf("Enter username:");
    fflush(stdout); 

    scanf("%256s", inputUsername);

    printf("Enter password:");
    fflush(stdout); 

    scanf("%256s", inputPassword);

    printf("Hello ");
    printf(inputUsername);
    fflush(stdout); 

    if(strcmp(inputUsername,username) == 0 && strcmp(inputPassword,password)==0)
    {
        //Get flag
        FILE *fd3 = fopen("/var/app/current/challenges/Reverse\ engineering/In\ good\ form/flag.txt", "r");
        fgets(flag, 64, fd3);

        printf("\nWelcome admin\n");
        printf("%s", flag);
        fflush(stdout);
    }
    else
    {
        printf("\nInvalid username and password");
    }
}


