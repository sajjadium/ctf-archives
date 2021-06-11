#include <stdio.h>
#include <unistd.h>

char shellcode[16];

int main() {
    char binsh[8] = "/bin/sh";

    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);

    printf("I'm trying to free your mind, Neo. But I can only show you the door. You're the one that has to walk through it.\n");
    read(0, shellcode, 16);

    ((void (*)()) (shellcode))();
}
