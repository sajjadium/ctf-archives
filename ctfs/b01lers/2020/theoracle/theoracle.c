#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void win() {
    char* argv[] = { NULL };
    char* envp[] = { NULL };

    execve("/bin/sh", argv, envp);
}

int main() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);

    char buffer[16];

    printf("Know Thyself.\n");
    fgets(buffer, 128, stdin);
}
