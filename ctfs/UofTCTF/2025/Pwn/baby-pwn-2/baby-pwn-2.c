#include <stdio.h>
#include <string.h>

void vulnerable_function()
{
    char buffer[64];
    printf("Stack address leak: %p\n", buffer);
    printf("Enter some text: ");
    fgets(buffer, 128, stdin);
}

int main()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    printf("Welcome to the baby pwn 2 challenge!\n");
    vulnerable_function();
    printf("Goodbye!\n");
    return 0;
}