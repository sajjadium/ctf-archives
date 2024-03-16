#include <stdio.h>
#include <unistd.h>

/* ignore this function */
void ignore()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

void get_flag() 
{
    char *args[] = {"/bin/cat", "flag.txt", NULL};
    execve(args[0], args, NULL);
}

int main() 
{
    ignore();
    char buf[0x20];
    printf("What's your name?\n>> ");
    gets(buf);
    printf("Hi %s!\n", buf);
    return 0;
}
