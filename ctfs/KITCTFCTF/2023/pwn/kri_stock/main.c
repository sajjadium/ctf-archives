#include <stddef.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>

#define ALARM_SECONDS 60

void be_a_ctf_challenge() {
    alarm(ALARM_SECONDS);
    setvbuf(stdout, (char *)0x0, 2, 1);
}

void koeri_choice(int data[7], int add) {
    int koeri_choice;
    int amount;
    int max_koeri = sizeof(*data) * sizeof(int);
    puts("Which kœri to add?");
    puts("[0] Sauce [1-6] Spice N");
    scanf("%d", &koeri_choice);
    if (koeri_choice < max_koeri) {
        puts("Amount");
        scanf("%d", &amount);
        if (add) {
            data[koeri_choice] += amount;
        } else {
            data[koeri_choice] -= amount;
            if (data[koeri_choice] < 0) {
                printf("Error, %d is an illegal value! Resetting to zero. Recount!\n",
                        data[koeri_choice]);
                data[koeri_choice] = 0;

            }
        }
    }
    else {
        puts("We do not have that kœri, yet");
    }
}

void print_stock(int data[7]) {
    for (int i = 0; i < 7; i++) {
        if (i == 0) {
            printf("Kœri sauce: %d\n", data[i]);
        }
        else {
            printf("Kœri spice no. %d: %d\n", i, data[i]);
        }
    }
}

int main(int argc, char** argv) {
    be_a_ctf_challenge();
    int choice;
    int data[7] = {0};
    while (1) {
        puts("[1] Add kœri to stock [2] Enter today's kœri consumption,\n[3] Print kœri stock [4] Exit");
        scanf("%d", &choice);
        if (choice == 1) {
            koeri_choice(data, 1);
        } else if (choice == 2) {
            koeri_choice(data, 0);
        } else if (choice == 3) {
            print_stock(data);
        } else if (choice == 4) {
            puts("Exiting...");
            break;
        } else {
            puts("Invalid choice");
        }
    }
    return 0;
}
