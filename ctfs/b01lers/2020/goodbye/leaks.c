#include <stdio.h>
#include <stdlib.h>

char name[16];

void yay() {
    asm("pop %rax");
    asm("syscall");
    return;
}

char * leak_stack_canary(char * buffer, int maxlen) {
    int length;

    scanf("%d", &length);
    if (length > maxlen) {
        exit(13);
    }

    fgetc(stdin);

    for (int i = 0; i <= length; i++) {
         buffer[i] = fgetc(stdin);
    }

    return buffer;
}

int main() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);

    char buffer[24];

    printf("You hear that, Mr. Anderson? That's the sound of inevitability, that's the sound of your death, goodbye, Mr. Anderson.\n");

    leak_stack_canary(name, 16);

    leak_stack_canary(buffer, 64);
    printf("%s\n", buffer);
    leak_stack_canary(buffer, 64);
    printf("%s\n", buffer);
    leak_stack_canary(buffer, 128);
    printf("%s\n", buffer);
}
