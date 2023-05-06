//
// Created by Jamie on 03/02/2021.
//

#include <stdio.h>
#include <iostream>
#include <algorithm>
#include <string.h>

#include "Animal.h"

Animal* animals[16] = {0};
int money = 500;
bool translator = false;

void* find_free(void** array, int szArray) {
    for (int i = 0; i < szArray; i++) {
        if (array[i] == NULL) {
            return &array[i];
        }
    }
    return NULL;
}

void* find_non_free(void** array, int szArray) {
    for (int i = 0; i < szArray; i++) {
        if (array[i] != NULL) {
            return &array[i];
        }
    }
    return NULL;
}

int menu() {
    unsigned int choice;
    printf("1) List Animals\n2) Act on Animal\n3) Buy New Animal\n4) Buy translator (1000c)\n5) Sell The Farm\n> ");
    std::cin >> choice;
    return choice;
}

void BuyAnimal(Animal** addr) {
    unsigned int choice;
    printf("1) Pig (150c)\n2) Cow (250c)\n> ");
    std::cin >> choice;
    Animal* animal;
    switch (choice) {
    case 1:
        if (money < COST_PIG) {
            puts("Can't afford pig");
            return;
        }
        animal = new Pig;
        animal->max_age = 18;
        strcpy(animal->type, "pig");
        money -= COST_PIG;
        break;
    case 2:
        if (money < COST_COW) {
            puts("Can't afford cow");
            return;
        }
        animal = new Cow;
        animal->max_age = 20;
        strcpy(animal->type, "pig");
        money -= COST_COW;
        break;
    default:
        puts("Unknown animal");
        return;
    }
    *addr = animal;
    animal->SetName();
    return;
}

void ActAnimal(Animal** addr) {
    unsigned int choice;
    printf("1) Sell\n2) Feed (50c)\n3) Rename (100c)\n4) Translate\n> ");
    std::cin >> choice;
    switch (choice) {
    case 1:
        money += addr[0]->Sell();
        delete addr[0];
        addr[0] = NULL;
        break;
    case 2:
        if (money < 50) {
            puts("Can't afford!");
            return;
        }
        addr[0]->hunger = 0;
        money -= 50;
        break;
    case 3:
        if (money < 100) {
            puts("Can't afford!");
            return;
        }
        addr[0]->SetName();
        money -= 100;
        break;
    case 4:
        if (translator) {
            addr[0]->Translate();
        } else {
            puts("You don't own this item");
        }
    default:
        puts("Unknown option");
    }
}

int main() {
    srand(time(NULL));
    setvbuf(stdout, NULL, _IONBF, 0);
    int choice;
    puts("Welcome to your new farm");
    for (;;) {
        printf("Your current balance is %d\n", money);
        choice = menu();
        if (choice == 1) {
            // List Animals
            Animal** addr = animals;
            int curIndex = 0;
            while (curIndex < sizeof(animals)/sizeof(animals[0])) {
                if (animals[curIndex] != NULL) {
                    printf("%d: ", curIndex);
                    animals[curIndex]->PrintInfo();
                }
                curIndex++;
            }
            puts("All animals introduced!");
        } else if (choice == 2) {
            // Act on Animal
            printf("Which animal? ");
            std::cin >> choice;
            choice = std::clamp(choice, 0, (int)(sizeof(animals)/sizeof(animals[0])));
            if (animals[choice] != NULL) {
                ActAnimal(&animals[choice]);
            } else {
                puts("No animal in that pen!");
            }
        } else if (choice == 3) {
            // Buy Animal
            Animal** addr = (Animal**)(find_free((void**)animals, sizeof(animals)/sizeof(animals[0])));
            if (addr == NULL) {
                puts("The farm is full");
                continue;
            }
            BuyAnimal(addr);
        } else if (choice == 4) {
            // Buy Translator
            if (money < COST_TRANSLATOR) {
                puts("Can't afford!");
                continue;
            }
            money -= COST_TRANSLATOR;
            translator = true;
            puts("Translator purchased");
        } else if (choice == 5) {
            // Quit
            puts("Goodbye!");
            return 0;
        }

        // Do Aging
        int curIndex = 0;
        while (curIndex < sizeof(animals)/sizeof(animals[0])) {
            if (animals[curIndex] != NULL) {
                animals[curIndex]->Age();
                if (animals[curIndex]->dead) {
                    delete animals[curIndex];
                    animals[curIndex] = NULL;
                }
            }
            curIndex++;
        }
    }

}