#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define NUM_BUYERS 8

struct spice_buyer {
    unsigned int spice_amount;
    char name[20];
};

unsigned int spice_amount(struct spice_buyer buyer) {
    /* TODO: convert to kilograms */
    return buyer.spice_amount;
}

void prompt(void) {
    char *prompt = 
        "Choose an option:\n"
        "(1) Add a buyer\n"
        "(2) Update a buyer's spice allocation\n"
        "(3) View a buyer\n"
        "(4) Deploy a hunter-seeker\n"
        "(5) Sell the spice\n";

    /* Never pass up an opportunity to practice your assembly skills! */
    asm volatile(
        "movq $1,   %%rax\n "
        "movq $1,   %%rdi\n "
        "movq %[s], %%rsi\n "
        "movq %[len], %%rdx\n "
        "syscall\n "
        :
        : [s]   "r" (prompt),
          [len] "r" (strlen(prompt))
        : "rax", "rdi", "rsi", "rdx"
    );
}

int main() {
    int i, num, len, spice;
    struct spice_buyer buyers[NUM_BUYERS];
    char buf[16];

    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    memset(buyers, 0, sizeof(buyers));

    srand(time(NULL));
    spice = rand() % 100;

    printf("House Harkonnen has finally taken control of Arrakis, and with it control of the crucial spice.\n");
    printf("However, the Baron poured all of his funds into exterminating House Atreides.\n");
    printf("Luckily, we sent some guys to drop the last of them into the desert, so that's all taken care of.\n");
    printf("\n");
    printf("For some reason our spice harvesters keep getting raided though?\n");
    printf("As a result, spice production is lower than expected.\n");
    printf("\n");
    printf("Can you help the Baron distribute the %d tons of spice among his prospective buyers?\n", spice);
    printf("\n");

    while (727) {
        prompt();
        printf("> ");

        fgets(buf, sizeof(buf), stdin);
        num = atoi(buf);

        switch (num) {
        case 1:
            printf("Enter the buyer index: ");
            fgets(buf, sizeof(buf), stdin);
            num = atoi(buf);

            if (num < 0 || num >= NUM_BUYERS) {
                printf("Invalid index!\n");
                continue;
            }

            printf("How long is the buyer's name? ");
            fgets(buf, sizeof(buf), stdin);
            len = atoi(buf);
            
            printf("Enter the buyer's name: ");
            fgets(buyers[num].name, len, stdin);
            buyers[num].name[strcspn(buyers[num].name, "\n")] = '\0';

            break;
        case 2:
            printf("Enter the buyer index: ");
            fgets(buf, sizeof(buf), stdin);
            num = atoi(buf);

            if (num < 0 || num >= NUM_BUYERS || strcmp(buyers[num].name, "") == 0) {
                printf("Invalid index!\n");
                continue;
            }

            printf("Enter the spice allocation (in tons) to this buyer: ");
            fgets(buf, sizeof(buf), stdin);
            buyers[num].spice_amount = atoi(buf);

            break;
        case 3:
            printf("Enter the buyer index: ");
            fgets(buf, sizeof(buf), stdin);
            num = atoi(buf);

            printf("Buyer %d: %s, allocated %u tons of spice\n", num, buyers[num].name, spice_amount(buyers[num]));

            break;
        case 4:
            printf("Your hunter-seeker explodes next to its target; before it explodes, here's what it saw: %p\n", buyers);

            break;
        default:
            for (i = 0; i < NUM_BUYERS; i++) {
                spice -= spice_amount(buyers[i]);
            }

            if (spice < 0) {
                printf("You oversold your spice resources. The Spacing Guild is extremely angry, and has revoked your shipping privileges.\n");
                goto done;
            } else if (spice == 0) {
                printf("You sold all of the spice! The Baron wanted you to sell it slowly to inflate the price! He is extremely angry with you.\n");
                goto done;
            } else {
                printf("You sold the spice, and have %d tons remaining. You live to see another day.\n", spice);
                goto done;
            }
        }
    }

done:
    return spice <= 0;
}

