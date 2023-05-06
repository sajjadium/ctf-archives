#include <stdio.h>
#include <stdlib.h>

#define LEEK 32

void cleanup(int a, int b, int c) {}

int main(void) {
    setbuf(stdout, NULL);
    FILE* leeks = fopen("/dev/null", "w");
    if (leeks == NULL) {
        puts("wtf");
        return 1;
    }
    printf("leek? ");
    char inp[LEEK];
    fgets(inp, LEEK, stdin);
    fprintf(leeks, inp);
    printf("more leek? ");
    fgets(inp, LEEK, stdin);
    fprintf(leeks, inp);
    printf("noleek.\n");
    cleanup(0, 0, 0);
    return 0;
}
