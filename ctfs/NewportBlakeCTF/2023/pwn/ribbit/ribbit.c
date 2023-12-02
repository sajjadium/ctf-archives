#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void win(long int jump_height, char* motivation) {
    FILE *fptr;
    char flag[64];

    fptr = fopen("flag.txt", "r");
    
    fgets(flag, 64, fptr);

    if (jump_height == 0xf10c70b33f && strncmp("You got this!", motivation, 13) == 0 && strncmp("Just do it!", motivation+21, 11) == 0) {
        puts("Thank you for helping my frog! Have a free flag in return.");
        puts(flag);
    } else {
        puts("You failed and flocto ate it :(");
        exit(0);
    }

    return;
}

void frog() {
    char motivation[25];

    puts("Can you give my pet frog some motivation to jump out the hole? ");

    gets(motivation);

    return;
}

int main() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    frog();

    return 0;
}
