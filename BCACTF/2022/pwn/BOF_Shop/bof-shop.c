#include <stdio.h>
#include <stdlib.h>

#define FLAG_BUFFER 100
int main() {
    char flag[FLAG_BUFFER];
    FILE *fp = NULL;
    char name[16];
    int balance = 0;
    
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    puts("Hello there, welcome to the BOF Shop!");
    puts("What's your name?");
    printf("> ");
    gets(name);

    printf("Your balance: %d coins\n\n", balance);

    if (balance != 100) {
        puts("Sorry, but you need exactly 100 coins to purchase the flag.\nGoodbye.");
        exit(1);
    }

    fp = fopen("flag.txt", "r");
    if (fp == NULL) {
        puts("Please add flag.txt to the present working directory to test this file.\n");
        puts("If you see this on the remote server, please contact admin.");
        exit(1);
    }

    fgets(flag, FLAG_BUFFER, fp);
    puts("Wow. Here, take the flag in exchange for your 100 coins.");
    puts(flag);
}
