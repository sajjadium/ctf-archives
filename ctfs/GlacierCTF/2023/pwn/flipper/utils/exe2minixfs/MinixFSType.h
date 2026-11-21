#pragma once

#include "FileSystemType.h"
#include "assert.h"

class MinixFSType : public FileSystemType
{
public:
    MinixFSType() :
        FileSystemType("minixfs")
    {

    }

    virtual ~MinixFSType()
    {

    }

    virtual Superblock *readSuper(Superblock *, void *) const
    {
        assert(0 && "Not implemented in exe2minixfs");
    }

    virtual Superblock *createSuper(uint32)
    {
        assert(0 && "Not implemented in exe2minixfs");
    }
};
