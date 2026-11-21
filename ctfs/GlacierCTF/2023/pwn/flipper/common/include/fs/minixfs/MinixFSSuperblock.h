#pragma once

#include "Superblock.h"
#include "MinixStorageManager.h"
#include "umap.h"

class Inode;
class MinixFSInode;
class Superblock;
class MinixFSType;

class MinixFSSuperblock : public Superblock
{
  public:
    friend class MinixFSInode;
    friend class MinixFSZone;
    friend class MinixStorageManager;

    MinixFSSuperblock(MinixFSType* fs_type, size_t s_dev, uint64 offset);
    virtual ~MinixFSSuperblock();

    /**
     * creates one new inode of the superblock
     * @param type the file type of the new inode (I_DIR, I_FILE)
     * @return the new inode
     */
    virtual Inode* createInode(uint32 type);

    /**
     * reads one inode from the mounted file system
     * @param inode the inode to read
     * @return 0 on success
     */
    virtual int32 readInode(Inode* inode);

    /**
     * writes the inode from the mounted file system
     * @param inode the inode to write
     */
    virtual void writeInode(Inode* inode);

    /**
     * removes one inode from the file system and frees all its resources
     * @param inode the inode to delete
     */
    virtual void deleteInode(Inode* inode);

    /**
     * add an inode to the all_inodes_ data structures
     * @param inode to add
     */
    void all_inodes_add_inode(Inode* inode);

    /**
     * remove an inode to the all_inodes_ data structures
     * @param inode to remove
     */
    void all_inodes_remove_inode(Inode* inode);

    /**
     * allocates one zone on the file system
     * @return the zone index
     */
    virtual uint16 allocateZone();

    /**
     * frees zone on the file system
     * @param index the zone index
     */
    virtual void freeZone(uint16 index);

  protected:

    /**
     * creates an Inode object with the given number from the file system
     * @param i_num the inode number
     * @return the Inode object
     */
    MinixFSInode *getInode(uint16 i_num);

    /**
     * creates an Inode object with the given number from the file system
     * this overloaded version should be used; directories usually have
     * "." and ".." entries, which are pointing to already loaded inodes!!!
     * by now this method is only called from MinixFSInode::loadChildren
     * @param i_num the inode number
     * @param is_already_loaded should be set to true if already loaded
     * @return the Inode object
     */
    MinixFSInode *getInode(uint16 i_num, bool &is_already_loaded);

    /**
     * reads one Zone from the file system to the given buffer
     * @param zone the zone index to read
     * @param buffer the buffer to write in
     */
    void readZone(uint16 zone, char *buffer);

    /**
     * reads the given number of blocks from the file system to the given buffer
     * @param block the index of the block to start reading
     * @param num_blocks the number of blcoks to read
     * @param buffer the buffer to write in
     */
    void readBlocks(uint16 block, uint32 num_blocks, char *buffer);

    /**
     * writes one zone from the given buffer to the file system
     * @param zone the zone index to write
     * @param buffer the buffer to write
     */
    void writeZone(uint16 zone, char *buffer);

    /**
     * writes the given number of blcoks to the file system from the given buffer
     * @param block the index of the first block to write
     * @param num_blocks the number of blocks to write
     * @param buffer the buffer to write
     */
    void writeBlocks(uint16 block, uint32 num_blocks, char *buffer);

    /**
     * writes the given number of bytes to the filesystem
     * the bytes must be on one block
     * @param block the block to write to
     * @param offset the offset on the block
     * @param size the number of bytes to write
     * @param buffer the buffer with the bytes to write
     * @return the number of bytes written
     */
    int32 writeBytes(uint32 block, uint32 offset, uint32 size, char *buffer);

    /**
     * reads the given number of bytes from the disc
     * the bytes must be on one block
     * @param block the block to read from
     * @param offset the offset on the block
     * @param size the number of bytes to read
     * @param buffer the buffer to write to
     * @return the number of bytes read
     */
    int32 readBytes(uint32 block, uint32 offset, uint32 size, char *buffer);

    /**
     * reads the fs header
     */
    void readHeader();
  private:

    /**
     * reads the root inode and its children from the filesystem
     */
    void initInodes();

    /**
     * # usable inodes on the minor device
     */
    uint32 s_num_inodes_;
    /**
     * # of blocks used by inode bit map
     */
    uint16 s_num_inode_bm_blocks_;
    /**
     * # of blocks used by zone bit map
     */
    uint16 s_num_zone_bm_blocks_;
    /**
     * number of first datazone
     */
    uint16 s_1st_datazone_;
    /**
     * log2 of blocks/zone
     */
    uint16 s_log_zone_size_;
    /**
     * maximum file size on this device
     */
    uint32 s_max_file_size_;

    uint32 s_zones_;

    uint16 s_block_size_;

    uint8 s_disk_version_;

    MinixStorageManager* storage_manager_;


    ustl::map<uint32, Inode*> all_inodes_set_;

    /**
     * pointer to self for compatability
     */
    Superblock* superblock_;

    /**
     * offset in the image file (in image util)
     */
    uint64 offset_;
};

