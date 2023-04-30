#include <stdio.h>
#include <stdlib.h>

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    static int seed = 69;
    srand(&seed);

    printf("Here's a lucky number: %p\n", &main);

    int lol = 1;
    int input = 0;
    for (int i = 1; i <= 7; ++i) {
        printf("Enter lucky number #%d:\n", i);
        scanf("%d", &input);
        if (rand() != input) {
            lol = 0;
        }
    }

    if (lol) {
        char flag[64] = {0};
        FILE* f = fopen("flag.txt", "r");
        fread(flag, 1, sizeof(flag), f);
        printf("Nice work, here's the flag: %s\n", flag);
    } else {
        puts("How unlucky :pensive:");
    }
}
