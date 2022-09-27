#ifndef FTOBJECT_H
#define FTOBJECT_H

#include <assert.h>
#include "ftallocator.h"

#define WHITE 0
#define GREY 2
#define BLACK 3

class FTObject
{

public:
    void *operator new(size_t size)
    {
        return FTAllocator::Alloc();
    }
    virtual void Mark() = 0;

    void SetGrey()
    {
        assert(this->IsWhite());
        this->markbits_ |= 2;
    }

    void SetBlack()
    {
        assert(this->IsGrey());
        this->markbits_ |= 3;
    }

    void UnsetMarkbits()
    {
        this->markbits_ = 0;
    }

    bool IsWhite()
    {
        return this->markbits_ == WHITE;
    }

    bool IsGrey()
    {
        return this->markbits_ == GREY;
    }

    bool IsBlack()
    {
        return this->markbits_ == BLACK;
    }

    void SetAlloc()
    {
        this->unalloc_ = false;
    }

    void UnsetAlloc()
    {
        this->unalloc_ = true;
    }

    bool IsAlloc()
    {
        return !this->unalloc_;
    }

private:
    char markbits_;
    bool unalloc_;
};

#endif