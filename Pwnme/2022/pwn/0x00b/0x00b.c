#include <stdio.h>
#include <stdlib.h>

void (*functions[2])(char *);
char user_input[100];

void get_input(char *buffer)
{
    fgets(buffer, 100, stdin);
}

void execute(char *buffer)
{
    system(buffer);
}

int main()
{
    puts("Fill the buffer:");
    fgets(user_input, 100, stdin);
    functions[0] = &puts;
    functions[1] = &get_input;

    char *input = NULL;
    size_t input_len = 0;

    char input_buffer[100];

    while (1)
    {
        printf("0: puts\n"
               "1: get_input\n"
               " >> ");
        if (getline(&input, &input_len, stdin) == -1)
            break;

        int choice = atoi(input);
        functions[choice](input_buffer);
    }
}