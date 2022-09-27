// gcc p0ison3d.c -o p0ison3d -fPIE -no-pie

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct note {
    int   allocated;
    char* data;
} note_t;

note_t storage[3];

void print_menu()
{
    printf("\n");

    puts("[1] add new note");
    puts("[2] read note");
    puts("[3] edit note");
    puts("[4] delete note");
    puts("[5] quit");
}

int get_choice()
{
    puts("choice:");

    int choice;
    if (!scanf("%d", &choice)) {
        return -1;
    }

    // flush stdin
    int c;
    while ((c = getchar()) != '\n' && c != EOF);

    return choice;
}

int get_index()
{
    puts("index:");

    int index;
    if (!scanf("%d", &index) ||
            (index < 0 || index >= 3)) {
        return -1;
    }

    // flush stdin
    int c;
    while ((c = getchar()) != '\n' && c != EOF);

    return index;
}

char* get_data(char* dest, int size)
{
    puts("data:");

    char* ret = fgets(dest, size, stdin);
    return ret;
}

void read_note()
{
    int index = get_index();
    if (index < 0) {
        puts("error: bad index");
        return;
    }
    if (!storage[index].allocated) {
        puts("error: index not allocated");
        return;
    }

    printf("data: %s\n", storage[index].data);
}

void add_note()
{
    int index = get_index();
    if (index < 0) {
        puts("error: bad index");
        return;
    }
    if (storage[index].allocated) {
        puts("error: index already allocated");
        return;
    }

    char* data = (char*)malloc(128);
    if (!get_data(data, 128)) {
        puts("error: unable to read input");
        return;
    }
    storage[index].data = data;
    storage[index].allocated = 1;
}

void edit_note()
{
    int index = get_index();
    if (index < 0) {
        puts("error: bad index");
        return;
    }
    if (!storage[index].allocated) {
        puts("error: index not allocated");
        return;
    }

    if (!get_data(storage[index].data, 153)) {
        puts("error: unable to read input");
        return;
    }
}

void del_note()
{
    int index = get_index();
    if (index < 0) {
        puts("error: bad index");
        return;
    }
    if (!storage[index].allocated) {
        puts("error: index not allocated");
        return;
    }

    free(storage[index].data);
    storage[index].data = NULL;
    storage[index].allocated = 0;
}

void quit()
{
    puts("\ngoodbye!");
    exit(0);
}

int main(int argc, char** argv)
{
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);

    puts("ez-notes v0.1");
    puts(" v0.1 only supports up to 3 notes :(");

    while (1) {
        print_menu();

        int choice = get_choice();
        if (choice < 0 || choice > 5) {
            puts("error: bad choice");
            continue;
        }
        
        if (choice == 1) {
            add_note();
        }
        if (choice == 2) {
            read_note();
        }
        if (choice == 3) {
            edit_note();
        }
        if (choice == 4) {
            del_note();
        }
        if (choice == 5) {
            quit();
        }
    }

    return 0;
}

void win()
{
    system("cat ./flag.txt");
}
