#include <unistd.h>
#include <stdio.h>

int main();

char buff[0x48];
void *const gift = main;

int main() {
    read(STDIN_FILENO, buff, 0x40);
    printf(buff);
}
