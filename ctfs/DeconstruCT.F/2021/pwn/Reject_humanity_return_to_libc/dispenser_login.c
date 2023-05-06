#include<stdio.h>
#include<string.h>

void disarm_dispenser(){
    char password[256];
    FILE *password_file;
    password_file = fopen("password.txt","r");
    fgets(password,sizeof(*password_file),password_file);
    printf("Enter password to disable dispenser:\n");
    char user_input[256];
    gets(user_input);
    int eq = strncmp(user_input,password,256);
    if (eq != 0) {
        printf("Incorrect password\n");
    }
    else {
        printf("Password correct\n");
        printf("Disarming dispenser (or not lol)...\n");
    }

}

int main() {
    disarm_dispenser();    
}
