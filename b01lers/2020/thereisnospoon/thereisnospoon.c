#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

char * xor(char * src, char * dest, int len) {
    for(int i = 0; i < len - 1; i++) {
        dest[i] = src[i] ^ dest[i];
    }
    dest[len-1] = 0;
    return dest;
}

int main() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);

    char buffer[256];
    int len = 256;

    printf("Neo, enter your matrix: ");
    len = read(0, buffer, len);

    char * buffer2 = malloc(strlen(buffer));

    int * changeme = malloc(sizeof(int));
    *changeme = 255;
    printf("Reality: %d\n", *changeme);
    
    printf("Make your choice: ");
    len = read(0, buffer2, len);

    printf("Now bend reality. Remember: there is no spoon.\n");
    char * result = xor(buffer2, buffer, len);
    printf("Result: %s\n", result);
    printf("Reality: %d\n", *changeme);

    if (*changeme != 0xff) {
        system("/bin/sh");
    }
}
