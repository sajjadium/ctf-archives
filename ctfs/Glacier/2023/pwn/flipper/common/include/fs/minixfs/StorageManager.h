#pragma once

#include "Bitmap.h"
#include "types.h"

class StorageManager
{
  public:

    /**
     * constructor
     * @param num_inodes the max number of inodes
     * @param num_zones the max number of zones
     */
    StorageManager(uint16 num_inodes, uint16 num_zones);

    virtual ~StorageManager();

    /**
     * frees the zone at the given index
     * @param index the zone index
     */
    virtual void freeZone(size_t index) = 0;

    /**
     * frees the inode at the given index
     * @param index the inode index
     */
    virtual void freeInode(size_t index) = 0;

    /**
     * checks if inode is set
     * @param index the inode index
     * @return true if the inode is set
     */
    virtual bool isInodeSet(size_t index) = 0;

  protected:

    Bitmap inode_bitmap_;
    Bitmap zone_bitmap_;

};

