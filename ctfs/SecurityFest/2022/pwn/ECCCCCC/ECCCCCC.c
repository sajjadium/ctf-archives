#include <stdio.h>
#include <stdlib.h>
#include <zlib.h>

struct region {
    char *data;
    size_t length;
};

struct region get_region() {
    struct region reg = {0};

    printf("Begin: ");
    scanf("%llx", &reg.data);

    printf("Length: ");
    scanf("%zu", &reg.length);

    return reg;
}

void print_hash() {
    puts("Please enter region to hash.");
    struct region to_hash = get_region();

    if (to_hash.length < 4)
        return puts("Sorry can't do that.");

    printf("hash: %lx\n", crc32(0L, to_hash.data, to_hash.length));
}

void correct_hash() {
    puts("Please enter region to correct.");
    struct region to_correct = get_region();

    if (to_correct.length < 4)
        return puts("Sorry can't do that.");

    printf("Correct hash: ");
    unsigned long correct = 0;

    scanf("%lu", &correct);

    for (int i = 0; i <= 0xff && crc32(0L, to_correct.data, to_correct.length) != correct; i++) {
        to_correct.data[0] = i;
    }

    if (crc32(0L, to_correct.data, to_correct.length) != correct) {
        puts("Could not correct the data!");
    }
    else {
        puts("Succesfully corrected the data!");
    }
}

int menu() {
    setvbuf(stdout, NULL, _IONBF, 0);

    puts("1. Print crc of region.");
    puts("2. Correct region.");

    int option = 0;
    printf("Option: ");
    scanf("%d", &option);

    return option;
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    puts("Welcome to the ECCCCCC (ECC Conventional Correction Control Center)");

    int option = 0;

    while (option = menu()) {
        switch (option) {
            case 1:
                print_hash();
                break;
            case 2:
                correct_hash();
                break;
            default:
                return puts("Invalid option.");
        }
    }
}
