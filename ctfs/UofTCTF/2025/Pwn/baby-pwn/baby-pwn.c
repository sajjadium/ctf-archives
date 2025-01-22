#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void secret()
{
    printf("Congratulations! Here is your flag: ");
    char *argv[] = {"/bin/cat", "flag.txt", NULL};
    char *envp[] = {NULL};
    execve("/bin/cat", argv, envp);
}

void vulnerable_function()
{
    char buffer[64];
    printf("Enter some text: ");
    fgets(buffer, 128, stdin);
    printf("You entered: %s\n", buffer);
}

int main()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    printf("Welcome to the Baby Pwn challenge!\n");
    printf("Address of secret: %p\n", secret);
    vulnerable_function();
    printf("Goodbye!\n");
    return 0;
}