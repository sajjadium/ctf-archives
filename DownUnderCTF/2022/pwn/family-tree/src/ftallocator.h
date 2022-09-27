#ifndef FTALLOCATOR_H_
#define FTALLOCATOR_H_

#include <stddef.h>
#include <vector>
#include <malloc.h>
#include <stdlib.h>
#include <list>

class Person;

using namespace std;

class FTAllocator
{

public:
    static void *Alloc();
    static void SetRoot(Person *p);
    static void Free(void *p);
    static void Init();
    static void Collect();
    static void Mark();
    static void Sweep();

private:
    static const size_t OBJSIZE = 256;
    static const size_t CAPACITY = 32;
    static void *heap_;
    static list<void *> free_list_;
    static Person *root_;
};
#endif