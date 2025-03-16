#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define NUM_SEENS 7

typedef struct {
    char name[20];
    int price;
} Seen;
int credit;

void displayMenu(Seen seens[]);
void addToBasket(Seen seens[], int quantities[]);
void checkout(Seen seens[], int quantities[]);

Seen seens[NUM_SEENS] = {
    {"Sabzeh", 30000},
    {"Senjed", 20000},
    {"Seer", 20000},
    {"Seeb", 10000},
    {"Samanu", 35000},
    {"Serkeh", 40000},
    {"Sekkeh", 80000000}
};

void topup(){
    puts("na bassete");
}

int main() {
    int quantities[NUM_SEENS] = {0};
    int choice;

    credit = 1000000;
    setbuf(stdin,NULL);
    setbuf(stdout,NULL);
    do {
        puts("Shop Menu:");
        puts("1. Add to Basket");
        puts("2. Checkout");
        puts("3. Top up");
        puts("4. Exit");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        
        switch (choice) {
            case 1:
                addToBasket(seens, quantities);
                break;
            case 2:
                checkout(seens, quantities);
                break;
            case 3:
                topup();
            case 4:
                return 0;
            default:
                puts("Invalid choice. Try again.");
        }
    } while (choice != 3);
    
    return 0;
}

void displayMenu(Seen seens[]) {
    puts("Available 7 Seens:");
    for (int i = 0; i < NUM_SEENS; i++) {
        printf("%d. %s - %d Toman\n", i + 1, seens[i].name, seens[i].price);
    }
}

void addToBasket(Seen seens[], int quantities[]) {
    int item, qty;
    displayMenu(seens);
    printf("Enter item number to add (1-7): ");
    scanf("%d", &item);
    if (item < 1 || item > NUM_SEENS) {
        puts("Invalid item.");
        return;
    }
    printf("Enter quantity: ");
    scanf("%d", &qty);
    if (qty < 1) {
        puts("Invalid quantity.");
        return;
    }
    quantities[item - 1] += qty;
    printf("Added %d %s(s) to your basket.\n", qty, seens[item - 1].name);
}

void checkout(Seen seens[], int quantities[]) {
    int total = 0;
    puts("Your Basket:");
    for (int i = 0; i < NUM_SEENS; i++) {
        if (quantities[i] > 0) {
            printf("%s - %d item = %d Toman\n", seens[i].name, quantities[i], seens[i].price * quantities[i]);
            total += seens[i].price * quantities[i];
        }
    }

    printf("Total: %d\n",total);
    if(total > credit){
        puts("Not enough credit.");
        exit(0);
    }

    if(quantities[6] > 10){
        puts("oh... pole ke mirize...");
        system("cat /flag");
    }
    puts("Thank you ~~ Have a nice Nowruz!");
    exit(0);
}
