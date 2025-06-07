#include <stdio.h>
#include <stdlib.h>

void gadget() {
    asm("push $0x69;pop %rdi");
}


void win(int secret) {
    if (secret == 0xA1B2C3D4) {
        system("/bin/sh");
    }
}


int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    unsigned int canary = 0xDEADBEEF;

    char buf[64];

    puts("I made a canary to stop buffer overflows. Prove me wrong!");
    gets(buf);

    if (canary != 0xDEADBEEF) {
        puts("No stack smashing for you!");
        exit(1);
    }


    return 0;
}
