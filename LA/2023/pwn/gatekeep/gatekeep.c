#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

void print_flag() {
    char flag[256];

    FILE* flagfile = fopen("flag.txt", "r");
    
    if (flagfile == NULL) {
        puts("Cannot read flag.txt.");
    } else {
        fgets(flag, 256, flagfile);
        flag[strcspn(flag, "\n")] = '\0';
        puts(flag);
    }
}

int check(){
    char input[15];
    char pass[10];
    int access = 0;

    // If my password is random, I can gatekeep my flag! :)
    int data = open("/dev/urandom", O_RDONLY);
    if (data < 0)
    {
        printf("Can't access /dev/urandom.\n");
        exit(1);
    }
    else
    {
        ssize_t result = read(data, pass, sizeof pass);
        if (result < 0)
        {
            printf("Data not received from /dev/urandom\n");
            exit(1);
        }
    }
    close(data);
    
    printf("Password:\n");
    gets(input);

    if(strcmp(input, pass)) {
        printf("I swore that was the right password ...\n");
    }
    else {
        access = 1;
    }

    if(access) {
        printf("Guess I couldn't gaslight you!\n");
        print_flag();
    }
}

int main(){
    setbuf(stdout, NULL);
    printf("If I gaslight you enough, you won't be able to guess my password! :)\n");
    check();
    return 0;
}
