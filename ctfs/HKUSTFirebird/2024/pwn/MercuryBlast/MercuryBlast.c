#include <unistd.h>
#include <malloc.h>
#include <stdio.h>

#define MAX_DESCRIPTION_SIZE 0x200
#define MAX_RECORDS 0x10

struct Record {
    double temperature;
    int description_size;
    char* description;
};

struct Record *records[MAX_RECORDS];

void add_record() {
    int i;
    for (i = 0; i < MAX_RECORDS; i++) {
        if (records[i] == NULL) {
            break;
        }
    }

    if (i == MAX_RECORDS) {
        puts("Too many records!");
        return;
    }

    int description_size;
    double temperature;
    printf("Input Temperature: ");
    scanf("%lf", &temperature);
    printf("Input Description Size: ");
    scanf("%d", &description_size);
    if (description_size > MAX_DESCRIPTION_SIZE) {
        puts("Description too long!");
        return;
    } else if (description_size <= 0) {
        puts("Invalid description size!");
        return;
    }

    struct Record *record = malloc(sizeof(struct Record));
    record->temperature = temperature;
    record->description_size = description_size;
    record->description = malloc(description_size);
    printf("Input Description: ");
    read(STDIN_FILENO, record->description, description_size);

    records[i] = record;

    puts("Record added!");
}

void delete_record() {
    printf("Input Index: ");
    int index;
    scanf("%d", &index);
    if (index < 0 || index >= MAX_RECORDS || records[index] == NULL) {
        puts("Invalid index!");
        return;
    }

    free(records[index]->description);
    free(records[index]);
    records[index] = NULL;

    puts("Record Deleted!");
}

void edit_record() {
    int index;
    printf("Input index: ");
    scanf("%d", &index);
    if (index < 0 || index >= MAX_RECORDS || records[index] == NULL) {
        puts("Invalid index!");
        return;
    }

    double temperature;
    int description_size;
    printf("Input Temperature: ");
    scanf("%lf", &temperature);
    printf("Input Description Size: ");
    scanf("%d", &description_size);
    if (description_size > MAX_DESCRIPTION_SIZE) {
        puts("Description too long!");
        return;
    } else if (description_size <= 0) {
        puts("Invalid description size!");
        return;
    }

    records[index]->temperature = temperature;
    records[index]->description_size = description_size;
    printf("Input Description: ");
    read(STDIN_FILENO, records[index]->description, description_size);

    puts("Record updated!");
}

void print_records() {
    int any_printed = 0;
    for (int i = 0; i < MAX_RECORDS; i++) {
        if (records[i] != NULL) {
            any_printed = 1;
            puts("==================================");
            printf("Record #%d\n", i);
            printf("Temperature: %lf\n", records[i]->temperature);
            printf("Description: ");
            write(STDOUT_FILENO, records[i]->description, records[i]->description_size);
            puts("");
        }
    }
    if (any_printed) {
        puts("==================================");
    }
}

void blast(char* buf) {
    read(STDIN_FILENO, buf, 0x20);
    free(buf+0x10);
}

void menu() {
    char mercury[0x20];
    while (1) {
        puts("1. Add record");
        puts("2. Print records");
        puts("3. Delete record");
        puts("4. Edit record");
        puts("0. Exit");
        printf("Your choice: ");

        scanf("%s", &mercury[0]);
        switch (mercury[0]) {
        case '1':
            add_record();
            break;
        case '2':
            print_records();
            break;
        case '3':
            delete_record();
            break;
        case '4':
            edit_record();
            break;
        case '0':
            puts("Bye!");
            return;
        case '\x7f':
            blast(mercury);
            break;
        default:
            puts("Invalid choice!");
            return;
        }
    }
}

void free_all_records() {
    for (int i = 0; i < MAX_RECORDS; i++) {
        if (records[i] != NULL) {
            free(records[i]->description);
            free(records[i]);
            records[i] = NULL;
        }
    }
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    alarm(60);

    puts("Welcome to the Temperature Records Management System!");
    puts("Our mercury thermometers are very fragile, so please be careful not to break anything!");

    menu();

    free_all_records();
    return 0;
}