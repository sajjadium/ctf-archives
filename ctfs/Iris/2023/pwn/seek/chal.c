#include <stdlib.h>
#include <stdio.h>

void win() {
    system("cat /flag");
}

int main(int argc, char *argv[]) {
    // This is just setup
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    printf("Your flag is located around %p.\n", win);

    FILE* null = fopen("/dev/null", "w");
    int pos = 0;
    void* super_special = &win;

    fwrite("void", 1, 4, null);
    printf("I'm currently at %p.\n", null->_IO_write_ptr);
    printf("I'll let you write the flag into nowhere!\n");
    printf("Where should I seek into? ");
    scanf("%d", &pos);
    null->_IO_write_ptr += pos;

    fwrite(&super_special, sizeof(void*), 1, null);
    exit(0);
}
