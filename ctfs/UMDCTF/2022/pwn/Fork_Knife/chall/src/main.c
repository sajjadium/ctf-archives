#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include "flask.h"
#include "helpers.h"

#define MIN_FLASKS 1
#define MAX_FLASKS 3

#define NUM_OPTIONS 4

void prompt_loop(void) {
    int choice, flask, order;
    size_t len;
    char arg[256];

    while (1) {
        printf("---- Menu ----\n");
        printf("1. Request ingredient\n");
        printf("2. Submit recipe\n");
        printf("3. Empty flask\n");
        printf("4. Exit\n");
        printf("Choice: ");

        choice = get_int();

        if (choice <= 0 || choice >= NUM_OPTIONS)
            goto cleanup;

        printf("Flask ID: ");
        flask = get_int();
        if (flask < MIN_FLASKS || flask > num_flasks)  {
            puts("Bad flask!");
            continue;
        }

        switch (choice) {
        case 1:
            printf("Order: ");
            order = get_int();
            if (order < 1 || order > MAX_ARGC) {
                puts("Bad order!");
                continue;
            }

            printf("Ingredient: ");
            len = get_line(arg, sizeof(arg));
            if (len >= MAX_ARGLEN) {
                puts("Ingredient too big!");
                continue;
            }

            flask_add(flask, order, arg, len);
            break;
        case 2:
            flask_mix(flask);
            break;
        case 3:
            flask_empty(flask);
            break;
        default:
            goto cleanup;
        }
    }

cleanup:
    puts("Goodbye!");

    clean_flasks();
    exit(EXIT_SUCCESS);
}

void signal_handler(int signum) {
    clean_flasks();
    exit(EXIT_SUCCESS);
}

int main(void) {
    int n;
    // buffering is cringe
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    // configure permissions
    // no ez root privesc :)
    setresgid(1000, 1001, 1001);
    setresuid(1000, 1001, 1001);

    // we will do what we can to kill excess children when xinetd sends signal
    struct sigaction new_action;
    new_action.sa_handler = signal_handler;
    sigemptyset(&new_action.sa_mask);
    new_action.sa_flags = 0;
    sigaction(SIGHUP, &new_action, NULL);
    sigaction(SIGTERM, &new_action, NULL);
    sigaction(SIGINT, &new_action, NULL);
    sigaction(SIGPIPE, &new_action, NULL);

    puts("-----------------------------------");
    puts("|      Fork n' Knife Brewery      |");
    puts("-----------------------------------");

    printf("Welcome to the brewery of mystics and mages!\n");
    printf("Please fill out the following form so we can service you.\n");

    printf("Number of flasks: ");
    n = get_int();

    if (n < MIN_FLASKS || n > MAX_FLASKS) {
        fprintf(stderr, "Come back later when you're feeling less greedy!\n");
        exit(EXIT_FAILURE);
    }

    printf("Summoning flasks...\n");
    init_flasks(n);

    prompt_loop();

    return 0;
}
