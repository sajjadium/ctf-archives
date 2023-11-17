// pwn/maltigriti
// by c0nrad - Sloppy Joe Pirates
// Enjoy <3

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char STATUS_ACCEPTED = 'A';
const char STATUS_REJECTED = 'R';
const char STATUS_DUPLICATE = 'D';

struct User {
    char name[32];
    char password[32];
    int bio_length;
    char *bio;
};

struct Report {
    struct User *user;
    char status;
    long bounty;
    char title[32];
    char body[128];
    struct Report *next;
};

void print_reports(struct Report *report) {
    int counter = 1;
    while (report != NULL) {
        printf("--- Report #%d ---\n", counter++);
        printf("Title: %s\n", report->title);
        printf("Body: %s\n", report->body);

        if (report->status == STATUS_ACCEPTED) {
            printf("Status: Accepted\n");
        } else if (report->status == STATUS_REJECTED) {
            printf("Status: Rejected\n");
        } else if (report->status == STATUS_DUPLICATE) {
            printf("Status: Duplicate\n");
        } else {
            printf("Status: Unknown\n");
        }

        printf("Bounty: %ld\n", report->bounty);
        report = report->next;
    }
}

void setup() {
    setvbuf(stdin, (char *)0x0, 2, 0);
    setvbuf(stdout, (char *)0x0, 2, 0);
    setvbuf(stderr, (char *)0x0, 2, 0);
}

void menu() {
    puts("\n\n--- Welcome to maltigriti's bug bounty reporting system! ---");
    puts("0. Register User");
    puts("1. Edit User");
    puts("2. Submit a bug report");
    puts("3. Print Reports");
    puts("4. Print Balance");
    puts("5. Buy Swag Pack");
    puts("6. Logout");
    puts("7. Exit");
    printf("menu> ");
}

void edit_user(struct User *user) {
    if (user != 0 && user->bio != NULL) {
        printf("Your current bio is: %s\n", user->bio);
        printf("Enter your new bio> ");
        fgets(user->bio, user->bio_length, stdin);
    } else {
        puts("You don't have a bio yet!");
        printf("How long is your bio> ");

        scanf("%d", &user->bio_length);
        getchar();

        user->bio = malloc(user->bio_length);
        printf("Enter your new bio> ");

        fgets(user->bio, user->bio_length, stdin);
    }
}

void logout(struct User *user) {
    if (user != NULL) {
        memset(user->name, 0, 32);
        memset(user->password, 0, 32);
        memset(user->bio, 0, user->bio_length);
        free(user->bio);
    }
}

int calculate_balance(struct Report *report, struct User *user) {
    int balance = 0;

    while (report != NULL) {
        if (report->status == STATUS_ACCEPTED && report->user == user) {
            balance += report->bounty;
        }
        report = report->next;
    }
    printf("Your balance is: %d\n", balance);
    return balance;
}

void buy_swag_pack(struct Report *report, struct User *user) {
    if (calculate_balance(report, user) >= 1337) {
        puts("You have enough money to buy a swag pack!");
        puts("With great swag comes great responsibility.");
        puts("Here is your swag pack: flag{redacted_redacted}");
        exit(0);
    } else {
        puts("You don't have enough money to buy a swag pack!");
        puts("Keep submitting bug reports and maybe you'll get there one day!");
        puts(":evil_grin:");
    }
}

struct User *register_user() {
    struct User *user = malloc(sizeof(struct User));

    printf("Enter your name> ");
    fgets(user->name, 32, stdin);

    printf("Enter your password> ");
    fgets(user->password, 32, stdin);

    edit_user(user);
    return user;
}

struct Report *new_report(struct Report *firstReport, struct User *user) {
    struct Report *report = malloc(sizeof(struct Report));

    if (firstReport != NULL) {
        // get last report
        struct Report *scanner = firstReport;
        while (scanner->next != NULL) {
            scanner = scanner->next;
        }
        scanner->next = report;
    } else {
        firstReport = report;
    }

    report->user = user;

    printf("Enter your report title> ");
    fgets(report->title, 32, stdin);

    printf("Please enter the content of your report> ");
    fgets(report->body, 128, stdin);

    // Automatically mark the status as duplicate so we don't have to pay anyone :evil_grin:
    report->status = STATUS_DUPLICATE;
    report->bounty = 0;

    puts("Thank you for submitting your bug report!");
    puts("Unfortunately our records indicate that this bug has already been submitted!");
    puts("Report will be closed and marked as duplicate.");
    puts("Hope you didn't spend too much time on it! ( ͡° ͜ʖ ͡°) ");

    return firstReport;
}

int main() {
    struct Report *reports = 0;
    struct User *user = 0;
    int report_count = 0;

    int menu_choice = 0;
    setup();
    while (1) {
        menu();
        scanf("%d", &menu_choice);
        getchar();

        switch (menu_choice) {
            case 0:
                user = register_user();
                break;
            case 1:
                edit_user(user);
                break;
            case 2:
                reports = new_report(reports, user);
                break;
            case 3:
                print_reports(reports);
                break;
            case 4:
                calculate_balance(reports, user);
                break;
            case 5:
                buy_swag_pack(reports, user);
                break;
            case 6:
                logout(user);
                break;
            case 7:
                exit(0);
                break;
            default:
                puts("Invalid choice!");
                break;
        }
    }
}
