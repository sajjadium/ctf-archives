 #include <malloc.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

char WASTE[32] = { 0 };
char TARGET[] = "Overwrite me!";

unsigned long read_num(void)
{
    char input[32] = { 0 };
    read(0, input, 0x1f);
    return strtoul(input, 0, 0);
}

void setup(void)
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void print_flag(void)
{
    char flag[] = "wsc{THIS_IS_NOT_THE_REAL_FLAG}";

    printf("%s\n", flag);
    exit(0);
}

int main(void)
{
    setup();
    char *_ptr = malloc(0x88);
    printf("Heap address @%p\n", _ptr - 0x10);
    printf("Target address @%p\n", TARGET);
    free(_ptr);


    unsigned long menu, size;
    while(1) {
        puts("\n1) malloc\n2) target\n3) quit\n> ");
        menu = read_num();

        if (menu == 1) {
            char *addr;
            puts("Size: ");
            size = read_num();
            addr = malloc(size);
            size = malloc_usable_size(addr);
            puts("Data: ");
            read(STDIN_FILENO, addr, size+8);
        } else if (menu == 2) {
            printf("\n%s\n", TARGET);
        } else if (menu == 3) {
            break;
        }

        if (!strcmp(TARGET, "I DID!")) {
            print_flag();
        }
    }
    return 1;
}
