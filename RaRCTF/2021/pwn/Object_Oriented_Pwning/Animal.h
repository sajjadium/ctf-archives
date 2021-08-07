//
// Created by Jamie on 03/02/2021.
//

#ifndef SRC_ANIMALS_H
#define SRC_ANIMALS_H
#include <stdint.h>
#include <stdio.h>

#define  MILK_BASE_VALUE 50

#define COST_COW 250
#define COST_PIG 150
#define COST_TRANSLATOR 1000

class Animal {
public:
    virtual void Age();
    virtual void PrintInfo();
    virtual int Sell() = 0;
    void Translate();
    void SetName();
    virtual ~Animal() = default;
    char type[16];
    bool dead = false;
    uint8_t max_age;
    uint8_t hunger = 0;
protected:
    uint8_t age = 1;
    char name[16];
};

class Pig : public Animal {
public:
    virtual int Sell();
    void SetName();
    virtual ~Pig() = default;
};
class Cow : public Animal {
public:
    virtual int Sell();
    void SetName();
    virtual ~Cow() = default;
};

void flush();
extern bool translator;
#endif //SRC_ANIMALS_H
