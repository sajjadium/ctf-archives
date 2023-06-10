// gcc chall.c -o chall

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define NUM_TEXTS 10
#define NUM_HEADERFOOTER_BYTES 24 // 16 header + 8 footer
#define MAX_BUFFER_SIZE 0x500

struct text
{
    char header[16];
    char buffer[];
    // There are actually 8 more footer bytes here, but flexible array members must be the last member
    // char footer[8];
};

struct text *texts[NUM_TEXTS] = {NULL};
int buffer_sizes[NUM_TEXTS] = {0};

void backdoor(const char *arg)
{
    // for debugging purposes
    system(arg);
}

void cleanup()
{
    // prevent memory leaks
    int idx;
    for (idx = 0; idx < NUM_TEXTS; idx++)
    {
        struct text *ptr = texts[idx];
        if (ptr != NULL)
        {
            free(ptr);
            texts[idx] = NULL;
        }
    }
}

void create()
{
    int idx;

    // find first empty text
    for (idx = 0; idx < NUM_TEXTS; idx++)
    {
        if (texts[idx] == NULL && buffer_sizes[idx] == 0)
        {
            break;
        }
    }
    if (idx == (NUM_TEXTS - 1))
    {
        puts("Not enough space.");
        return;
    }

    puts("What size?");
    unsigned int buffer_size;
    scanf("%i", &buffer_size);

    if (buffer_size > MAX_BUFFER_SIZE)
    {
        puts("Size too large.");
        exit(EXIT_FAILURE);
    }

    struct text *ptr = malloc(buffer_size + NUM_HEADERFOOTER_BYTES); // account for header + footer data
    if (ptr == NULL)
    {
        puts("malloc error");
        exit(EXIT_FAILURE);
    }

    texts[idx] = ptr;
    buffer_sizes[idx] = buffer_size;

    puts("What content?");
    read(0, ptr->buffer, buffer_size);
    memcpy(ptr->header, "=======\nmessage:", 16);
    long *footer = (long *)&ptr->buffer[buffer_size];
    memcpy(footer, "=======\n", 8);
}

void output()
{
    int idx;
    puts("Which text? (0-9)");
    scanf("%d", &idx);

    unsigned int buffer_size;
    struct text *ptr;

    if (idx >= 0 && idx < NUM_TEXTS)
    {
        buffer_size = buffer_sizes[idx];
        ptr = texts[idx];
    }

    if (ptr == NULL)
    {
        puts("Create text first.");
        return;
    }

    write(1, ptr, buffer_size + NUM_HEADERFOOTER_BYTES);
}

void update()
{
    int idx;
    puts("Which text? (0-9)");
    scanf("%d", &idx);

    unsigned int buffer_size;
    struct text *ptr;

    if (idx >= 0 && idx < NUM_TEXTS)
    {
        buffer_size = buffer_sizes[idx];
        ptr = texts[idx];
    }

    if (ptr == NULL)
    {
        puts("Create text first.");
        return;
    }

    read(0, &(ptr->buffer), buffer_size);
}

void delete()
{
    int idx;
    puts("Which text? (0-9)");
    scanf("%d", &idx);

    if (idx >= 0 && idx <= 9)
    {
        unsigned int buffer_size = buffer_sizes[idx];
        buffer_sizes[idx] = 0;
        if (buffer_size != 0)
        {
            buffer_sizes[idx] = 0;
        }

        struct text *ptr = texts[idx];
        if (ptr != NULL)
        {
            free(ptr);
            texts[idx] = NULL;
            atexit(cleanup); // free ALL pointers on exit
        }
    }
}

int main()
{
    setbuf(stdout, 0);
    setbuf(stdin, 0);

    const char menu[] = "1. [C]reate\n2. [O]utput\n3. [U]pdate\n4. [D]elete\n5. [E]xit\n";
    char choice;
    while (choice != 'E')
    {
        write(1, menu, sizeof(menu));
        scanf(" %c", &choice);
        switch (choice)
        {
        case 'C':
            create();
            break;
        case 'O':
            output();
            break;
        case 'U':
            update();
            break;
        case 'D':
            delete ();
            break;
        }
    }

    exit(0);
}