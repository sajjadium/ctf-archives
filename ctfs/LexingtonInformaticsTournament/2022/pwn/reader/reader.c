#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int n;

int menu(){
    puts("Your options are:");
    puts("1) read");
    puts("2) show");
    puts("3) exit");
    
    puts("What would you like to do?");

    int x;
    scanf("%d", &x);
    getchar();
    puts("");

    return x;
}

void invalid(char *mes){
    printf("Invalid %s.\n", mes);
    _exit(1);
}

void reads(char s[]){
    puts("Here's where I read your stuff.\n");

    puts("Input what you'd like to have read:");
    read(0, s, n + 0x28);
    puts("");

    puts("Input read.\n");
}

void show(char s[]){
    puts("Here I show you what I've read from you.\n");

    puts("Here's what I've read:");
    puts(s);
    puts("");

    puts("Input shown.\n");
}

int main(){
    puts("Welcome to my reader challenge.\n");

    puts("How much do you want read today?");
    scanf("%d", &n);
    puts("");

    char *s = alloca(n);

    puts("Ok.\n");

    for(int x = 0; x != 3;){
        x = menu();
        switch(x){
            case 1:
                reads(s);
                break;
            case 2:
               	show(s);
                break;
            case 3:
                puts("Bye.");
                break;
            default:
                invalid("option, does not exist");
                break;
        }
    }
    
    return 0;
}
