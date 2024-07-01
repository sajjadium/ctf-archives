#include "alloc.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum {
    REFUND_DENIED,
    REFUND_APPROVED,
} refund_status_t;

typedef struct refund_request {
    refund_status_t status;
    int amount;
    char reason[0x80];
} refund_request_t;


refund_request_t *requests[10] = {NULL};

void print_flag() {
    char flag[64];
    FILE *f = fopen("flag.txt", "r");
    if (f == NULL) {
        puts("Flag file not found.");
        return;
    }

    fgets(flag, 64, f);
    printf("%s\n", flag);
    fclose(f);
}

void handle_complaint() {
    puts("Please enter your complaint:");
    char *trash = pwnymalloc(0x48);
    fgets(trash, 0x48, stdin);
    memset(trash, 0, 0x48);
    pwnyfree(trash);
    puts("Thank you for your feedback! We take all complaints very seriously.");
}

void handle_view_complaints() {
    puts("Oh no! Our complaint database is currently down. Please try again later.");
}

void handle_refund_request() {
    int request_id = -1;
    for (int i = 0; i < 10; i++) {
        if (requests[i] == NULL) {
            request_id = i;
            break;
        }
    }

    if (request_id == -1) {
        puts("Sorry, we are currently unable to process any more refund requests.");
    }

    refund_request_t *request = pwnymalloc(sizeof(refund_request_t));
    puts("Please enter the dollar amount you would like refunded:");
    char amount_str[0x10];
    fgets(amount_str, 0x10, stdin);
    sscanf(amount_str, "%d", &request->amount);

    puts("Please enter the reason for your refund request:");
    fgets(request->reason, 0x80, stdin);
    request->reason[0x7f] = '\0'; // null-terminate

    puts("Thank you for your request! We will process it shortly.");
    request->status = REFUND_DENIED;

    requests[request_id] = request;

    printf("Your request ID is: %d\n", request_id);
}

void handle_refund_status() {
    puts("Please enter your request ID:");
    char id_str[0x10];
    fgets(id_str, 0x10, stdin);
    int request_id;
    sscanf(id_str, "%d", &request_id);

    if (request_id < 0 || request_id >= 10) {
        puts("Invalid request ID.");
        return;
    }

    refund_request_t *request = requests[request_id];
    if (request == NULL) {
        puts("Invalid request ID.");
        return;
    }

    if (request->status == REFUND_APPROVED) {
        puts("Your refund request has been approved!");
        puts("We don't actually have any money, so here's a flag instead:");
        print_flag();
    } else {
        puts("Your refund request has been denied.");
    }
}

int main() {
    // disable buffering
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    puts("Welcome to the SIGPwny Transit Authority's customer service portal! How may we help you today>");

    while (1) {
        puts("\n1. Submit a complaint");
        puts("2. View pending complaints");
        puts("3. Request a refund");
        puts("4. Check refund status");
        puts("5. Exit\n");

        printf("> ");
        char choice_str[0x10];
        fgets(choice_str, 0x10, stdin);
        int choice;
        sscanf(choice_str, "%d", &choice);

        switch (choice) {
            case 1: 
                handle_complaint();
                break;
            case 2:
                handle_view_complaints();
                break;
            case 3:
                handle_refund_request();
                break;
            case 4:
                handle_refund_status();
                break;
            case 5:
                exit(0);
            default:
                puts("Invalid choice. Try again.");
        }
    }
}