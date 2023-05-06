//
// Created by Jamie on 03/02/2021.
//

#include "Animal.h"
#include <cstdlib>
#include <cmath>
#include <stdio.h>
#include <iostream>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/syscall.h>

void flush() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

void Animal::Age() {
    this->age += (rand() % 3) + 1;
    this->hunger += (rand() % 3) + 1;
    if (this->age >= this->max_age) {
        printf("[-----] %s has died of old age! [-----]\n", this->name);
        this->dead = true;
    } else if (this->hunger >= 20) {
        printf("[-----] %s has died of hunger! [-----]\n", this->name);
        this->dead = true;
    }
}

void Animal::Translate() {
    char buf[1024];
    sprintf(buf, "/usr/games/cowsay -f ./%s.txt 'Feed me!'", this->type);
    system(buf);
}

void Animal::SetName() {
    printf("What will you name your new animal? ");
    flush();
    unsigned char c;
    int read = 0;
    while ((c = getchar()) != '\n' && read < 64) {
        this->name[read] = c;
        read++;
    }
}

void Animal::PrintInfo() {
    printf("%s (Age: %d, Hunger: %d/15)\n", this->name, this->age, this->hunger);
}

int Cow::Sell() {
    int middle = this->max_age / 2;
    int max = COST_COW * 5;
    if (this->age == middle) {
        return max;
    }
    return std::round(max/std::abs(this->age - middle));
}

int Pig::Sell() {
    int middle = this->max_age / 2;
    int max = COST_PIG * 5;
    if (this->age == middle) {
        return max;
    }
    return std::round(max/std::abs(this->age - middle));
}
