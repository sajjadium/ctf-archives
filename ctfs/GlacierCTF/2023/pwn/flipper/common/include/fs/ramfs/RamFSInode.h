#pragma once

#include "types.h"
#include "fs/Inode.h"

class RamFSInode : public Inode
{
  protected:
    char* data_;

  public:
    /**
     * constructor
     * @param super_block the superblock to create the inode on
     * @param inode_type the inode type
     */
    RamFSInode ( Superblock *super_block, uint32 inode_type );
    virtual ~RamFSInode();

    /**
     * Called when a file is opened
     */
    virtual File* open(Dentry* dentry, uint32 /*flag*/);

    /// read the data from the inode
    /// @param offset offset byte
    /// @param size the size of data that read from this inode
    /// @buffer the dest char-array to store the data
    /// @return On successe, return 0. On error, return -1.
    virtual int32 readData ( uint32 offset, uint32 size, char *buffer );

    /// write the data to the inode
    /// @param offset offset byte
    /// @param size the size of data that write to this inode (data_)
    /// @buffer the src char-array
    /// @return On successe, return 0. On error, return -1.
    virtual int32 writeData ( uint32 offset, uint32 size, const char *buffer );

};

