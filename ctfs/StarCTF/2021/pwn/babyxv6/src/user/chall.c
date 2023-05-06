#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

int readnum() {
    char buf[0x20] = {0};
    read(0, buf, 0x10);
    return atoi(buf);
}

void challenge()
{
    int size;
    char input[0x80];

    printf("Welcome to babystack 2021!\n");
    printf("How many bytes do you want to send?\n");
    
    size = readnum();
    if (size > 0x1000) {
        printf("You are greedy!\n");
        return;
    }

    printf("show me your input\n");
    read(0, input, 0x80);
    baby(input, size);

    printf("It's time to say goodbye.\n");
    return;
}

int main(int argc, char *argv[])
{
    challenge();
    exit(0);
}
