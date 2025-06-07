#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

#define MAX_LEN 32
#define FLAG_FILE "./flag.txt"
#define FLAG_SIZE 256

const char *SECRET = "[REDACTED]";

void changeGrade() {
    char buf[FLAG_SIZE];
    memset(buf, 0, FLAG_SIZE);
    FILE *f = fopen(FLAG_FILE, "r");
    if (f == NULL) {
        printf("Missing flag file. \n");
    } else {
        fgets(buf, FLAG_SIZE, f);
        printf("\n");
        printf("Whose grade would you like to change?");
        printf("\n");
        write(STDOUT_FILENO, buf, strlen(buf));
        printf("\n");
    }
    exit(0);
}

void accessMemory() {
    struct timespec ts = {.tv_sec = 0, .tv_nsec = 5000000};
    nanosleep(&ts, NULL);
}

void authenticateTeacher() {
    char input[MAX_LEN];
    printf("\n[TEACHER VIEW] Enter your password [a-z, 0-9]:");
    scanf("%31s", input);

    for (int i = 0; i < strlen(SECRET); i++) {
        accessMemory();
        if (input[i] != SECRET[i]) break;
        accessMemory();
    }

    if (strcmp(input, SECRET) == 0) {
        printf("\nAccess granted.\n");
        changeGrade();
    } else {
        printf("\nInvalid password!\n");
    }
}

void showGrade(int id) {
    switch ((short)id) {
        case 1: printf("Phineas: A+\n"); break;
        case 2: printf("Ferb: A\n"); break;
        case 3: printf("Candace: B+\n"); break;
        case 4: printf("Buford: C\n"); break;
        case 5: printf("Baljeet: A+\n"); break;
        case 6: printf("Isabella: A\n"); break;
        case 7: printf("Perry: P\n"); break;
        case 8: printf("Doofenshmirtz: D\n"); break;
        case 9: printf("Jeremy: B\n"); break;
        case 10: printf("Vanessa: A-\n"); break;
        case 0x0BEE:
            printf("\nAccessing teacher view...\n");
            authenticateTeacher();
            break;
        default:
            printf("Unknown student ID.\n");
    }
}

int main() {
    setvbuf(stdin,  NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    int id;
    printf("Welcome to the Tri-State Grade Viewer\n");
    printf("Enter your student ID: ");

    if (scanf("%d", &id) != 1 || id > 10) {
        printf("Invalid student ID.\n");
        int ch;
        while ((ch = getchar()) != '\n' && ch != EOF);
        exit(0);
    }
    
    showGrade(id);
    return 0;
}
