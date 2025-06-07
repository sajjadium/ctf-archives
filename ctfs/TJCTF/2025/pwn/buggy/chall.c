#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>


#define DEBUG true

int main(int argc, char **argv) {
    char inputBuffer[1024];
    unsigned int balance = 50;
    
    setbuf(stdout, NULL);

    if (DEBUG) {
        printf("%p, %p\n", &inputBuffer, &balance);
    }

    puts("Welcome to TJ Bank!");
    while (true) {
        printf("What would you like to do? (view balance|deposit|withdraw|transfer|exit) ");
        fgets(inputBuffer, 1024, stdin);
        if (strcmp(inputBuffer, "view balance\n") == 0) {
            printf("Your balance is $%u\n", balance);
        } else if (strcmp(inputBuffer, "deposit\n") == 0) {
            printf("Enter amount: ");
            fgets(inputBuffer, 1024, stdin);
            if (DEBUG) {
                printf(inputBuffer);
            }
            int amount = atoi(inputBuffer);
            balance += amount;
            printf("$%u added to account\n", amount);
        } else if (strcmp(inputBuffer, "withdraw\n") == 0) {
            printf("Enter amount: ");
            fgets(inputBuffer, 1024, stdin);
            if (DEBUG) {
                printf(inputBuffer);
            }
            int amount = atoi(inputBuffer);
            if (amount > balance) {
                puts("Balance too low to continue. Aborting.");
                continue;
            }
            balance -= amount;
            printf("$%u removed from account\n", amount);
        } else if (strcmp(inputBuffer, "transfer\n") == 0) {
            printf("Enter account number for transfer: ");
            fgets(inputBuffer, 1024, stdin);
            int accountNumber = atoi(inputBuffer);
            printf("Enter amount: ");
            fgets(inputBuffer, 1024, stdin);
            int amount = atoi(inputBuffer);
            if (amount > balance) {
                puts("Balance too low to continue. Aborting.");
                continue;
            }
            balance -= amount;
            printf("$%u transferred to account number %u\n", amount, accountNumber);
        } else if (strcmp(inputBuffer, "exit\n") == 0) {
            break;
        } else {
            puts("Please enter a valid option");
        }
    }
    return 0;
}