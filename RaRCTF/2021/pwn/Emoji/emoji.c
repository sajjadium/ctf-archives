#define _CRT_SECURE_NO_WARNINGS
#include <unistd.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

ssize_t read(int fd, void *buf, size_t count);
ssize_t write(int fd, const void *buf, size_t count);

typedef struct __attribute__((__packed__)) EmojiEntry {
    uint8_t data[4];
    char* title;
} entry;

entry* entries[8] = {0};
void* garbage[50] = {0};

int find_free_slot(uint64_t * arr, int size) {
    for (int i = 0; i < size; i++) {
        if (arr[i] == 0) {
            return i;
        }
    }
    return -1;
}

int menu() {
    printf("Emoji DB v 2.1\n1) Add new Emoji\n2) Read Emoji\n3) Delete Emoji\n4) Collect Garbage\n> ");
    unsigned int res;
    scanf("%ud\n", &res);
    return res;
}

int count_leading_ones(unsigned char i) {
    int count = 0;
    while ((i & 0b10000000) > 0) {
        count += 1;
        i = i << 1;
    }
    return count;
}

void add_emoji() {
    int i = find_free_slot((uint64_t *)entries, sizeof(entries));
    if (i < 0) {
        puts("No free slots");
        return;
    }
    entry* new_entry = (entry *)malloc(sizeof(entry));
    new_entry->title = malloc(0x80);
    printf("Enter title: ");
    read(0, new_entry->title, 0x80 - 1);
    new_entry->title[0x80-1] = '\0';
    printf("Enter emoji: ");
    read(0, new_entry->data, 1);
    read(0, new_entry->data+1, count_leading_ones(new_entry->data[0]) - 1);
    entries[i] = new_entry;
}

void read_emoji() {
    printf("Enter index to read: ");
    unsigned int index;
    scanf("%ud", &index);
    if (index > sizeof(entries) | entries[index] == NULL) {
        puts("Invalid entry");
        return;
    }
    printf("Title: %s\nEmoji: ", entries[index]->title);
    write(1, entries[index]->data, count_leading_ones(entries[index]->data[0]));

}

void delete_emoji() {
    printf("Enter index to delete: ");
    unsigned int index;
    scanf("%ud", &index);
    if (index > sizeof(entries) | entries[index] == NULL) {
        puts("Invalid entry");
        return;
    }
    int i = find_free_slot((uint64_t *)garbage, sizeof(garbage));
    garbage[i] = entries[index];
    int i2 = find_free_slot((uint64_t *)garbage, sizeof(garbage));
    garbage[i2] = entries[index]->title;
    entries[index]->title = NULL;
    entries[index] = NULL;

}

void collect_garbage() {
    for (int i = 0; i < sizeof(garbage); i++) {
        if (garbage[i] != NULL) {
            free(garbage[i]);
            garbage[i] = NULL;
        }
    }
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    int c = menu();
    while (c < 5) {
        switch (c) {
        case 1:
            add_emoji();
            break;
        case 2:
            read_emoji();
            break;
        case 3:
            delete_emoji();
            break;
        case 4:
            collect_garbage();
            break;
        default:
            puts("Unknown option");
        }
        c = menu();
    }
}

