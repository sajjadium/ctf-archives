#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <sys/types.h>

typedef struct phone_number {
    uint16_t country_code; // +64 in New Zealand
    uint16_t area_code;    // 4 for Wellington landlines
    uint16_t local_number_1; // usually 3 digits
    uint16_t local_number_2; // usually 4 digits
} phone_number_t;

#define VUW_PHONE_NUMBER (phone_number_t){.country_code = 64, .area_code = 4, .local_number_1 = 472, .local_number_2 = 1000}

void print_phone_number(const phone_number_t *phone) {
    printf("Phone Number: +%d %d %d-%d",
           phone->country_code,
           phone->area_code,
           phone->local_number_1,
           phone->local_number_2);
}

int decode_from_string(const char *str, phone_number_t *phone) {
    if (sscanf(str, "+%hu %hu %hu-%hu",
               &phone->country_code,
               &phone->area_code,
               &phone->local_number_1,
               &phone->local_number_2) != 4) {
        return 0; // fail
    }
    return 1;
}

void clear_line() {
    // clear until end of line
    int throwaway;
    do {
        throwaway = getchar();
    } while (throwaway != '\n' && throwaway != EOF);
}

#define MAX_PHONEBOOK_SIZE (size_t)16

typedef struct phonebook {
    size_t size;
    phone_number_t entries[MAX_PHONEBOOK_SIZE];
} phonebook_t;

int main() {
    phonebook_t phonebook = { .size = 0 };

    phonebook.entries[phonebook.size++] = VUW_PHONE_NUMBER;

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    printf("---=== kiwiphone ===---\n");
    printf("The kiwi phonebook utility\n\n");
    printf("Launching phonebook app\n");

    while (1) {
        printf("\nPhonebook size: %zu\n", phonebook.size);
        for (size_t i = 0; i < phonebook.size; i++) {
            printf("Entry %02zu: ", i + 1);
            print_phone_number(&phonebook.entries[i]);
            printf("\n");
        }

        printf("\nEnter the index of the entry to write,\n");
        printf("or -1 to exit:\n");
        int index;
        if (scanf(" %d", &index) != 1) {
            printf("Invalid input\n");
            clear_line();
            continue;
        }

        if (index == -1) {
            break; // exit
        }

        clear_line();

        if (index < 0 || index > phonebook.size) {
            if (phonebook.size < MAX_PHONEBOOK_SIZE) {
                phonebook.size++; // attempt to grow by one
            }

            if (index < 0 || index > phonebook.size) {
                // still didn't fit after trying to grow
                printf("Out of bounds!\n");
                continue;
            }
        }

        printf("Enter the phone number to store: \n");

        char *line = NULL;
        size_t alloc_len = 0;
        ssize_t nread = getline(&line, &alloc_len, stdin);
        if (nread == -1) {
            free(line);
            printf("Unexpected error\n");
            exit(EXIT_FAILURE);
        }
        line[nread - 1] = '\0'; // Remove newline character

        if (!decode_from_string(line, &phonebook.entries[index - 1])) { // zero-indexed array
            free(line);
            printf("Phone number format error\n");
            continue;
        }

        free(line);
    }

    printf("\nExiting phonebook app\n");
}