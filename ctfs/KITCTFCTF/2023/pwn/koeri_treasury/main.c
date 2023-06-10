#include <stddef.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include "koeri_crypt.h"

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
        }
    }
    else {
        puts("We do not have that kœri, yet");
    }
}

int main(int argc, char** argv) {
    be_a_ctf_challenge();
    int choice;
    int data[7] = {0};
    koeri_crypt_init(data);

    // encryption is costly
    char* encrypted_flag = koeri_encrypt_flag();
    while (1) {
        puts("[1] Add kœri to stock [2] Enter today's kœri consumption,\n[3] Print encrypted flag [4] Exit");
        scanf("%d", &choice);
        if (choice == 1) {
            koeri_choice(data, 1);
        } else if (choice == 2) {
            koeri_choice(data, 0);
        } else if (choice == 3) {
            puts(encrypted_flag);
        } else if (choice == 4) {
            puts("Exiting...");
            break;
        } else {
            puts("Invalid choice");
        }
    }
    return 0;
}
