#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

void init() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
}

void win() {
    system("/bin/sh");
}

int main() {
    init();

    printf("Free junk: 0x%lx\n", init);
    printf("Your turn: ");

    char buf[0x10];
    read(0, buf, 0x11);
}
