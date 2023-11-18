#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char command_buf[128];

char *copy_command_to_buf(char *command,  char *buf)
{
    strcpy(buf, command);
}

void cat_flag()
{
    copy_command_to_buf("cat flag.txt", command_buf);
}

void ls()
{
    copy_command_to_buf("ls -lh flag.txt", command_buf);
}

void shasum_flag()
{
    copy_command_to_buf("shasum flag.txt", command_buf);
}

void do_the_thing(char *the_thing)
{
    system(the_thing);
}

int main(void)
{
    puts("Welcome to the ROPL!");

    while (1)
    {
        puts("what thing would you like to do?\n1: ls -lh flag.txt\n2: shasum flag.txt");
        char choice[16];
        fgets(choice, 9999, stdin);
        if (choice[0] == '1')
        {
            ls();
            do_the_thing(command_buf);
        }
        else if (choice[0] == '2')
        {
            shasum_flag();
            do_the_thing(command_buf);
        }
        else
        {
            break;
        }
    }
}