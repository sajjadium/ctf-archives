#include <stdio.h>
#include <stdlib.h>

int check(unsigned long n, unsigned long sold) {
    if ((n & 0xffff) == (sold & 0xffff)) {
        return 1;
    }
    return 0;
}

void vuln() {
    unsigned long num_sold;
    char resp;
    unsigned long a;
    unsigned long b;
    unsigned long c;
    unsigned long d;
    
    num_sold = rand();

    printf("It's not that easy though, enter 4 numbers to use to guess!\n");
    
    do {
        // ask user for input
        printf("1st number: ");
        scanf("%lu", &a);
        printf("2nd number: ");
        scanf("%lu", &b);
        printf("3rd number: ");
        scanf("%lu", &c);
        printf("4th number: ");
        scanf("%lu", &d);

        // perform some calculations on the numbers
        d = d + c;
        c = c ^ b;
        b = b - a;

        if (check(d, num_sold)) {
                printf("Woohoo! That's exactly how many she sold!\n");
                printf("Here's a little something Sally wants to give you for your hard work: %lx\n", &d);
        } else {
                printf("Sorry, that's not quite right :(\n");
        }

        // go again?
        printf("Would you like to guess again? (y/n) ");
        scanf("%s", &resp);

    } while (resp == 'Y' || resp == 'y');

    return;
}

void welcome() {
    printf("Sally sold some sea SHELLS!\n");
    printf("Try to guess exactly how many she sold, I bet you can't!!\n");
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    welcome();
    vuln();
    
    printf("'bye now'\n-Sally\n");
    return 0;
}
