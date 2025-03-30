#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>

#define BUF_SIZE 20
#define MAX_ALLOCS 100

typedef struct Alloc {
    unsigned char * data;
    uint64_t len;
} Alloc;

Alloc allocs[MAX_ALLOCS];
int current_index = 0;

void menu() {
    write(1, "1. Alloc\n", 9);
    write(1, "2. Free\n", 8);
    write(1, "3. View\n", 8);
    write(1, "4. Exit\n", 8);
}

void alloc_chunk() {
    char buf[BUF_SIZE];
    unsigned int size = 0;
    if (current_index >= MAX_ALLOCS) {
        write(1, "Out of space!\n", 14);
        return;
    }
    write(1, "Size?\n> ", 8);
    read(0, buf, BUF_SIZE);
    size = strtoul(buf, NULL, 10);
    if (size > 0x800) {
        write(1, "Too big!\n", 9);
        return;
    }
    allocs[current_index].data = malloc(size);
    allocs[current_index].len = 0;

    write(1, "Data?\n> ", 8);
    size_t amt_read = read(0, allocs[current_index].data, size);
    if (amt_read > 0) {
        allocs[current_index].len = amt_read;
    }

    current_index++;
    write(1, "Done!\n", 6);
}

void free_chunk() {
    char buf[BUF_SIZE];
    unsigned int i = 0;
    write(1, "Index?\n> ", 9);
    read(0, buf, BUF_SIZE);
    i = strtoul(buf, NULL, 10);
    if (i < MAX_ALLOCS) {
        free(allocs[i].data);
        allocs[i].len = 0;
    } else {
        write(1, "Invalid index!\n", 15);
        return;
    }
    write(1, "Done!\n", 6);
}

void view_chunk() {
    char buf[BUF_SIZE];
    unsigned int i = 0;
    write(1, "Index?\n> ", 9);
    read(0, buf, BUF_SIZE);
    i = strtoul(buf, NULL, 10);
    if (i < MAX_ALLOCS && allocs[i].data != NULL && allocs[i].len > 0) {
        write(1, allocs[i].data, allocs[i].len);
    } else {
        write(1, "Invalid index!\n", 15);
    }
}

int main() {
    char buf[BUF_SIZE];
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);

    write(1, "You're in a locked room. Can you escape?\n", 41);
    write(1, "I'll say it in red: \x1B[31mIn this room, you can only malloc and free. Your goal is to escape and reach the flag.\x1B[0m\n", 116);
    write(1, "I'll say it in blue: \x1B[36mWith the hardened allocator, it is impossible to escape! You will be stuck here forever!\x1B[0m\n", 119);

    while (1) {
        menu();
        write(1, "> ", 2);
        unsigned long choice = 0;
        read(0, buf, BUF_SIZE);
        choice = strtoul(buf, NULL, 10);
        switch (choice) {
            case 1:
                alloc_chunk();
                break;
            case 2:
                free_chunk();
                break;
            case 3:
                view_chunk();
                break;
            case 4:
                write(1, "\x1B[31mYou are incompetent!\x1B[0m\n", 30);
            default:
                _exit(0);
        }
    }
    return 0;
}