// Compile with `gcc -static -fno-tree-loop-distribute-patterns -nostdlib -O3 -o example example.c sdk.c`

#include "sdk.h"

int main() {
    char *buf = malloc(256);
    print("Vad heter du?\n> ");
    size_t len = read(buf, 256);
    {
        int i = 0;
        while (i < 255 && buf[i] != '\n') i++;
        buf[i] = 0;
    }
    print("Hej ");
    print(buf);
    print("!\n");
    return 0;
}
