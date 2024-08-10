#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int get(char* buf, int n) {
    fflush(stdout);
    if (fgets(buf, n, stdin) == NULL) {
        puts("Error");
        exit(1);
    }
    int end = strcspn(buf, "\n");
    if (buf[end] == '\0') {
        puts("Too long");
        exit(1);
    }
    buf[end] = '\0';
    return end;
}

int main(void) {
    fputs("Filename? ", stdout);
    char fname[10];
    int fn = get(fname, sizeof(fname));
    for (int i = 0; i < fn; ++i) {
        char c = fname[i];
        if (('a' <= c && c <= 'z') || c == '.') {
            continue;
        }
        puts("Only a-z and .");
        return 1;
    }
    if (strstr(fname, "flag.txt") != NULL) {
        printf("Nice try!");
        return 1;
    }
    FILE* file = fopen(fname, "a+b");

    fputs("Read (R) or Write (W)? ", stdout);
    char option[3];
    get(option, sizeof(option));

    switch (option[0]) {
        case 'R': {
            char contents[25];
            int n = fread(contents, 1, sizeof(contents), file);
            fputs("Contents: ", stdout);
            fwrite(contents, 1, n, stdout);
            puts("");
            break;
        }
        case 'W': {
            fputs("Contents? ", stdout);
            char contents[25];
            int n = get(contents, sizeof(contents));
            fwrite(contents, 1, n, file);
            break;
        }
        default: {
            puts("Invalid");
            return 1;
        }
    }

    fclose(file);
    fflush(stdout);

    int ret = system("gcc main.c -o main");
    if (!WIFEXITED(ret) || WEXITSTATUS(ret)) {
        puts("Compilation failed");
        return 1;
    }
    execl("main", "main", NULL);
}
