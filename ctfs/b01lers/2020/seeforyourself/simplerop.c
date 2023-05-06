#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

char * binsh = "/bin/sh";

int main() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
    system(NULL);

    char * shellcode[0];

    printf("Unfortunately, no one can be told what the Matrix is. You have to see it for yourself.\n");
    read(0, shellcode, 64);
}
