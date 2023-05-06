#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>

void win() {
    system("/bin/sh");
}

void init() {
    alarm(60);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main(void) {
    char your_try[64]={0};
    char flag[64]={0};

    init();

    puts("guess the flag!> ");

    FILE *fp = fopen("./flag", "r");
    if (fp == NULL) exit(-1);
    size_t length = fread(flag, 1, 64, fp);

    scanf("%64s", your_try);

    if (strncmp(your_try, flag, length) == 0) {
        puts("yes");
        win();
    } else {
        puts("no");
    }
    return 0;
}
