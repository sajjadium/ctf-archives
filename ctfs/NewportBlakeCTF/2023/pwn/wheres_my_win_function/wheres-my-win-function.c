#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

int main() {
    char answer[0x100];

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);

    printf("wheres my win function?\n");

    return gets(answer);    
}