#pragma once

#include "StorageManager.h"
#include "types.h"
#include "minix_fs_consts.h"

class MinixFSSuperblock;

class MinixStorageManager : public StorageManager
{
  public:

    /**
     * constructor
     * @param bm_buffer the buffer with the inode and zone bitmaps from disc
     * @param num_inode_bm_blocks the number of blocks used for the inode bitmap
     * @param num_zone_bm_blocks the number of blocks used for the zone bitmap
     * @param num_inodes the max number of inodes
     * @param num_zones the max number of zones
     */
    MinixStorageManager(char *bm_buffer, uint16 num_inode_bm_blocks, uint16 num_zone_bm_blocks, uint16 num_inodes,
                        uint16 num_zones);

    virtual ~MinixStorageManager();

    virtual size_t allocZone();
    virtual size_t allocInode();
    virtual void freeZone(size_t index);
    virtual void freeInode(size_t index);
    virtual bool isInodeSet(size_t index);
    virtual uint32 getNumUsedInodes();
    void flush(MinixFSSuperblock *superblock);
    void printBitmap();

  private:

    size_t curr_zone_pos_;
    size_t curr_inode_pos_;

    uint32 num_inode_bm_blocks_;
    uint32 num_zone_bm_blocks_;

};


