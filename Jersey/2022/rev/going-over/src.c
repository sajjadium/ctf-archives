#include <stdio.h>
#include <unistd.h>

void grab_ledge()
{
    puts("ayy we made it");
    execve("/bin/sh", NULL, NULL);
}

int main(void)
{
    char action[12];

    setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);

    puts("We thought it was a good idea to go white-water rafting...");
    puts("but now we're about to go over a waterfall!!");
    puts("HELP!!!!!");
    puts("The map said there was a ledge nearby that we could escape to but I can't find it!!!");

    gets(action);
    printf("Let's try this %s and hope it works D:\n", action);
}