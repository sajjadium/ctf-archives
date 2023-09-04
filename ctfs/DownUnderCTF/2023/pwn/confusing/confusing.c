#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void init() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
}

int main() {
    init();

    short d;
    double f;
    char s[4];
    int z; 

    printf("Give me d: ");
    scanf("%lf", &d);

    printf("Give me s: ");
    scanf("%d", &s);

    printf("Give me f: ");
    scanf("%8s", &f);

    if(z == -1 && d == 13337 && f == 1.6180339887 && strncmp(s, "FLAG", 4) == 0) {
        system("/bin/sh");
    } else {
        puts("Still confused?");
    }
}
