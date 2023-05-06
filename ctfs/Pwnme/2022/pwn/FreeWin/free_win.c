#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct
{
    char header[0x20]; // Not used yet, but will be used in order to specify the type of the entry
    int (*function)(const char *);
    char *buffer;
    int size;
} * entries[0x10] = {0};

void get_str(char *buffer, int length)
{
    printf(" >> ");
    fflush(stdout);
    fgets(buffer, length, stdin);

    // Set last character to 0 if it is a newline
    size_t len = strlen(buffer);
    if (buffer[len - 1] == '\n')
        buffer[len - 1] = 0;
}

int get_int(int min, int max)
{
    char input[0x10];
    get_str(input, 0x10);

    int int_input = atoi(input);

    if (int_input > max || int_input < min)
    {
        fprintf(stderr, "Incorrect input\n");
        exit(-1);
    }
}

int menu()
{
    puts("Welcome to FreeWin !");
    puts("");
    puts("  1.  Malloc");
    puts("  2.  Free");
    puts("  3.  Edit");
    puts("  4.  Execute");
    puts("");
    fflush(stdout);

    int choice = get_int(1, 4);

    return choice;
}

void malloc_chunk()
{
    puts("Index:");
    int index = get_int(0, 0x10);

    entries[index] = malloc(sizeof(**entries));

    puts("Size:");
    entries[index]->size = get_int(0x10, 0x100);

    puts("Buffer:");
    printf("%d\n", entries[index]->size);
    entries[index]->buffer = malloc(entries[index]->size);
    get_str(entries[index]->buffer, entries[index]->size);

    // TODO: Add options on function -> Let the user choose between different functions
    entries[index]->function = puts;
}

void free_chunk()
{
    puts("Index:");
    int index = get_int(0, 0x10);

    char *buffer = entries[index]->buffer;

    free(entries[index]);
    free(buffer);
}

void edit_chunk()
{
    puts("Index:");
    int index = get_int(0, 0x10);

    puts("Buffer:");
    get_str(entries[index]->buffer, entries[index]->size);
}

void execute_chunk()
{
    puts("Index:");
    int index = get_int(0, 0x10);

    entries[index]->function(entries[index]->buffer);
}

// Not used yet, but will be used in a later version as a choice between different functions
int execute_chunk_ping(char *buffer)
{
    char cmd[0x100] = {0};
    sprintf(cmd, "ping -c 1 %s", buffer);

    system(cmd);

    return 0;
}

int main()
{
    for (int choice = menu(); choice; choice = menu())
    {
        switch (choice)
        {
        case 1:
            malloc_chunk();
            break;

        case 2:
            free_chunk();
            break;

        case 3:
            edit_chunk();
            break;

        case 4:
            execute_chunk();
            break;

        default:
            fprintf(stderr, "An error happened\n");
            fflush(stderr);
            exit(-1);
        }
    }
}