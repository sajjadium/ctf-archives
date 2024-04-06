#include <stdio.h>
#include <stdlib.h>

void print_flag();
void print_ufsit_info();
void print_pwn_info();

int main() {
    int user_option;
    int is_admin = 0;
    char username[15];
    
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    
    printf("Please enter your username to login.\n"
           "Username:");

    // I saw something online about this being vulnerable???
    // The blog I read said something about how a buffer overflow could corrupt other variables?!?
    // Eh whatever, It's probably safe to use here.
    gets(username);

    printf("Welcome %s!\n\n", username);

    if(is_admin == 0){
        printf("User %s is not a system admin!\n\n", username);
    } else {
        printf("User %s is a system admin!\n\n", username);
    }

    printf("In order to run a command, type the number and hit enter!\n");

    // This loop repeats forever
    // I hope the user never want's to log out
    while(1){
        printf("What command would you like to run?\n"
               "1 - Print Information About UFSIT\n"
               "2 - Print Information About Binary Exploitation (PWN)\n"
               "3 - Print The Flag\n"
               "4 - Exit The Program\n"
               ">");

        scanf("%d", &user_option);

        if(user_option == 1){
            print_ufsit_info();
        }

        if(user_option == 2){
            print_pwn_info();
        }

        if(user_option == 3){
            // Check to see if the user is not an admin.
            if(is_admin == 0){
                printf("Sorry! You are not an admin!\n");
            } else{
                print_flag();
            }
        }

        if(user_option == 4){
            printf("Goodbye!\n");
            exit(0);
        }

        printf("\n");
    }
}

void print_flag(){
    FILE* ptr;
    char str[50];
    ptr = fopen("flag.txt", "r");

    if (NULL == ptr) {
        printf("file can't be opened, please let SwampCTF admins know if you see this!\n");
		exit(1);
    }

    printf("Here is your flag!\n");

    while (fgets(str, 50, ptr) != NULL) {
        printf("%s\n", str);
    }

    fclose(ptr);
    return;
}

void print_ufsit_info(){
    printf("UFSIT is UFs cybersecurity and hacking club!\n\n"
           "Discord: https://discord.gg/7HFp3fVWJh\n"
           "Instagram: https://www.instagram.com/uf.sit/\n"
           "Website: https://www.ufsit.club/\n"
           "\n"
           "UFSIT is the beginner friendly cybersecurity  club at the University of Florida. Our goal is to help get "
           "student interested in the field!"
           "\n");
    return;
}

void print_pwn_info(){
    printf("Binary exploitation is the art of subverting the expectations of the original programmer. By providing "
           "a program with input that it doesn't know how to handle you can bend it until it breaks. "
           "This could be in the form of exploiting a logic bug or spotting something that the original programmer missed. "
           "When people think of hacking they think of binary exploitation. Now this may sound intimidating, but sometimes"
           " it's just a simple as overflowing a buffer."
           "\n\n"
           "Hacking isn't a toolset, it's a mindset.\n");
    return;
}
