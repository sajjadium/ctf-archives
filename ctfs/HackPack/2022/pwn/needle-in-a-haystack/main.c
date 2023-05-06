#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "main.h"

#define ARRAY_SIZE 100000

const static char *flagString = "givemetheflagpls";

bool existsInString(char *needle, char *buf) {
    return strstr(buf, needle);
}

void invalidInput() {
    printf("no hacking pls!!!1111!\n");
    exit(-1);
}

int main(int argc, char **argv) {
    char *buf = malloc(ARRAY_SIZE);
    printf("prepare to write to buffer at: %p\n", buf);
    printf("please enter your super secret string: ");
    fflush(stdout);
    fgets(buf, ARRAY_SIZE, stdin);

    if(existsInString(flagString, buf)) {
        printf("only admins are allowed to use the *super secret* string\n");
        invalidInput();
    }

    if(strstr(buf, flagString)) {
        printf("welcome, you must be an admin!\n");
        FILE *flagFile = fopen("flag.txt", "r");
        if(flagFile == NULL) {
            fprintf(stderr, "error opening flag file, please contact an administrator (this is not part of the challenge)\n");
            exit(-1);
        }
        fgets(buf, ARRAY_SIZE, flagFile);
        printf("here's your flag... %s\n", buf);
    } else {
        printf("hmmm, seems you don't know the secret phrase -- you're probably not supposed to be here :)\n");
    }

    free(buf);
}