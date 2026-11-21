#pragma once

#include "FileSystemType.h"

class MinixFSType : public FileSystemType
{
  public:
    MinixFSType();
    virtual ~MinixFSType();

    /**
     *  reads the superblock from the device
     * @param superblock a pointer to the resulting superblock
     * @param data the data given to the mount system call
     * @return the superblock
     */
    virtual Superblock *readSuper(Superblock *superblock, void *data) const;

    /**
     * creates an Superblock object for the actual file system type
     * @param root the root dentry
     * @param s_dev the device number
     */
    virtual Superblock *createSuper(uint32 s_dev);
};

