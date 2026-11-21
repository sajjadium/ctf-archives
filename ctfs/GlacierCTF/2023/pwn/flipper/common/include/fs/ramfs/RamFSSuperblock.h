#pragma once

#include "fs/Superblock.h"

class Inode;
class Superblock;
class RamFSType;

class RamFSSuperblock : public Superblock
{
  public:
    /**
     * constructor
     * @param s_root the root dentry of the new filesystem
     * @param s_dev the device number of the new filesystem
     */
    RamFSSuperblock (RamFSType* type, uint32 s_dev );
    virtual ~RamFSSuperblock();

    /**
     * create a new Inode of the superblock, mknod with dentry, add in the list.
     * @param dentry the dentry to create the new inode with
     * @param type the inode type
     * @return the inode
     */
    virtual Inode* createInode (uint32 type );

    /**
     * This method is called to read a specific inode from a mounted file-system.
     * @param inode the inode to read
     * @return 0 on success
     */
    virtual int32 readInode ( Inode* inode );

    /**
     * This method is called to write a specific inode to a mounted file-system,
     * and gets called on inodes which have been marked dirty.
     * @param inode the inode to write
     */
    virtual void writeInode ( Inode* inode );

    /**
     * This method is called whenever the reference count on an inode reaches 0,
     * and it is found that the link count (i_nlink= is also zero. It is
     * presumed that the file-system will deal with this situation be
     * invalidating the inode in the file-system and freeing up any resourses
     * used.
     * @param inode the inode to delete
     */
    virtual void deleteInode ( Inode* inode );
};
//-----------------------------------------------------------------------------

