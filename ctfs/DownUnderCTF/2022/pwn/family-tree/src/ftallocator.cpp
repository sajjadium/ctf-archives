
#include "ftallocator.h"
#include "ftobject.h"
#include "person.h"
#include <iostream>
#include <string.h>

Person *FTAllocator::root_ = 0;
void *FTAllocator::heap_ = (void *)malloc(FTAllocator::OBJSIZE * FTAllocator::CAPACITY);
list<void *> FTAllocator::free_list_;

void FTAllocator::Init()
{
    for (size_t i = 0; i < CAPACITY; i++)
    {
        void *p = FTAllocator::heap_ + i * FTAllocator::OBJSIZE;
        FTAllocator::free_list_.push_front(p);
    }
}

void *FTAllocator::Alloc()
{
    void *ptr;
    ptr = FTAllocator::free_list_.back();
    FTAllocator::free_list_.pop_back();
    ((FTObject *)ptr)->SetAlloc();
    memset(ptr + 2,0, FTAllocator::OBJSIZE-2);

    if (FTAllocator::free_list_.size() == 0)
    {
        FTAllocator::Collect();
        if (FTAllocator::free_list_.size() == 0)
        {
            printf("OOM\n");
            exit(-1);
        }
    }
    return ptr;
}

void FTAllocator::SetRoot(Person *p)
{
    FTAllocator::root_ = p;
}

void FTAllocator::Free(void *p)
{
    if (((FTObject *)p)->IsAlloc())
    {
        ((FTObject *)p)->UnsetAlloc();
        FTAllocator::free_list_.push_back(p);
    }
}

void FTAllocator::Mark()
{
    FTAllocator::root_->Mark();
}

void FTAllocator::Sweep()
{
    for (size_t i = 0; i < FTAllocator::CAPACITY; i++)
    {
        FTObject *o = (FTObject *)(FTAllocator::heap_ + i * FTAllocator::OBJSIZE);
        if (!o->IsWhite())
        {
            o->UnsetMarkbits();
        }
        else
        {
            Free(o);
        }
    }
}

void FTAllocator::Collect()
{
    FTAllocator::Mark();
    FTAllocator::Sweep();
}