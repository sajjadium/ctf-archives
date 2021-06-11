#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <assert.h>

#define DO_STAGE(num, cond) do {\
    printf("Stage " #num ": ");\
    scanf("%lu", &converter.uint);\
    x = converter.dbl;\
    if(cond) {\
        puts("Stage " #num " passed!");\
    } else {\
        puts("Stage " #num " failed!");\
        return num;\
    }\
} while(0);

void print_flag() {
    FILE* flagfile = fopen("flag.txt", "r");
    if (flagfile == NULL) {
        puts("Couldn't find a flag file.");
        return;
    }
    char flag[128];
    fgets(flag, 128, flagfile);
    flag[strcspn(flag, "\n")] = '\x00';
    puts(flag);
}

union cast {
    uint64_t uint;
    double dbl;
};

int main(void) {
    union cast converter;
    double x;

    DO_STAGE(1, x == -x);
    DO_STAGE(2, x != x);
    DO_STAGE(3, x + 1 == x && x * 2 == x);
    DO_STAGE(4, x + 1 == x && x * 2 != x);
    DO_STAGE(5, (1 + x) - 1 != 1 + (x - 1));

    print_flag();

    return 0;
}
