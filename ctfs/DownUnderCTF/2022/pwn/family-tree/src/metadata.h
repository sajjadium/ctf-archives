#ifndef METADATA_H_
#define METADATA_H_

#include "ftallocator.h"

#define METADATA_SZ 240


class Metadata : FTObject
{

public:
    Metadata() {}

    void *operator new(size_t size)
    {

        return FTAllocator::Alloc();
    }
    void Mark()
    {
        // set straight to black as we know there are no children
        this->SetGrey();
        this->SetBlack();
    }

    char data[METADATA_SZ];
};

#endif