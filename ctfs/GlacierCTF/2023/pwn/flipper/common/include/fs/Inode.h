#pragma once

#include "types.h"
#include "kprintf.h"
#include <ulist.h>
#include <uatomic.h>
#include "Dentry.h"
#include "assert.h"

class File;
class Superblock;

/**
 * three possible inode state bits:
 */
#define I_UNUSED 0 // the unused inode state
#define I_DIRTY 1 // Dirty inodes are on the per-super-block s_dirty_ list, and
// will be written next time a sync is requested.
#define I_LOCK 2  //state not implemented

#define A_READABLE  0x0001
#define A_WRITABLE  0x0002
#define A_EXECABLE  0x0004

/**
 * five possible inode type bits:
 */
#define I_FILE         0
#define I_DIR          1
#define I_LNK          2
#define I_CHARDEVICE   3
#define I_BLOCKDEVICE  4

/**
 * The per-inode flags:
 */
#define MS_NODEV 2 // If this inode is a device special file, it cannot be
// opend.
#define INODE_DEAD 666

class Inode
{
  protected:
    ustl::list<Dentry*> i_dentrys_;

    /**
     * The (open) file of this inode.
     */
    ustl::list<File*> i_files_;

    /**
     * the number of Dentry links to this inode.
     */
    uint32 i_nlink_;

    /**
     * the number of runtime references to this inode (loaded Dentrys, open files, ...)
     */
    uint32 i_refcount_;

    Superblock *superblock_;

    /**
     * current file size in bytes
     */
    uint32 i_size_;

    /**
     * Inode type: I_FILE, I_DIR, I_LNK, ...
     */
    uint32 i_type_;

    /**
     * There are three possible inode state bits: I_DIRTY, I_LOCK, I_UNUSED.
     */
    uint32 i_state_;
     
    /**
     * The inodes permission flag
     */
    uint32 i_mode_;
  public:

    /**
     * contructor
     * @param super_block the superblock to create the inode on
     * @param inode_type the inode type
     */
    Inode(Superblock *super_block, uint32 inode_type);

    virtual ~Inode();

    uint32 incRefCount();
    uint32 decRefCount();
    uint32 numRefs();

    uint32 incLinkCount();
    uint32 decLinkCount();
    uint32 numLinks();

    void addDentry(Dentry* dentry);
    void removeDentry(Dentry* dentry);
    bool hasDentry(Dentry* dentry);


    /**
     * lookup should check if that name (given by the char-array) exists in the
     * directory (I_DIR inode) and should return the Dentry if it does.
     * This involves finding and loading the inode. If the lookup failed to find
     * anything, this is indicated by returning NULL-pointer.
     * @param name the name to look for
     * @return the dentry found
     */
    virtual Dentry* lookup(const char* /*name*/);

    /**
     * Called when a file is opened
     */
    virtual File* open(Dentry* /*dentry*/, uint32 /*flag*/)
    {
      return 0;
    }

    /**
     * Called when the last reference to a file is closed
     */
    virtual int32 release(File* /*file*/);

    /**
     * This should create a symbolic link in the given directory with the given
     * name having the given value. It should d_instantiate the new inode into
     * the dentry on success.
     * @param inode the inode to link to
     * @param dentry yhe dentry to create the link in
     * @param link_name the name of the link to create
     * @return 0 on success
     */
    virtual int32 symlink(Inode */*inode*/, Dentry */*dentry*/, const char */*link_name*/)
    {
      return 0;
    }

    /**
     * Create a directory with the given dentry.
     * @param the dentry
     * @return 0 on success
     */
    virtual int32 mkdir(Dentry *);

    /**
     * Create a file with the given dentry.
     * @param dentry the dentry
     * @return 0 on success
     */
    virtual int32 mkfile(Dentry */*dentry*/);

    /**
     * Create a special file with the given dentry.
     * @param the dentry
     * @return 0 on success
     */
    virtual int32 mknod(Dentry*);

    /**
     * Create a hard link with the given dentry.
     * @param the dentry
     * @return 0 on success
     */
    virtual int32 link(Dentry*);

    /**
     * Unlink the given dentry from the inode.
     * @param the dentry
     * @return 0 on success
     */
    virtual int32 unlink(Dentry*);

    /**
     * Remove the named directory (if empty).
     * @return 0 on success
     */
    virtual int32 rmdir(Dentry*);

    /**
     * change the name to new_name
     * @param new name the new name
     * @retunr 0 on success
     */
    virtual int32 rename(const char* /*new_name*/)
    {
      return 0;
    }

    /**
     * The symbolic link referred to by the dentry is read and the value is
     * copied into the user buffer (with copy_to_user) with a maximum length
     * given by the integer.
     * @param dentry the dentry
     * @param max_length the maximum length
     * @return the number of bytes read
     */
    virtual int32 readlink(Dentry */*dentry*/, char*, int32 /*max_length*/)
    {
      return 0;
    }

    /**
     * If the directory (parent dentry) have a directory and a name within that
     * directory (child dentry) then the obvious result of following the name
     * from the directory would arrive at the child dentry. (for symlink)
     * @param prt_dentry the parent dentry
     * @param chd_dentry the child dentry
     * @return the dentry
     */
    virtual Dentry* followLink(Dentry */*prt_dentry*/, Dentry */*chd_dentry*/)
    {
      return 0;
    }

    /**
     * read the data from the inode
     * @param offset the offset from where to start
     * @param size the number of bytes to read
     * @param buffer where to store the read data
     * @return the number of bytes read
     */
    virtual int32 readData(uint32 /*offset*/, uint32 /*size*/, char */*buffer*/)
    {
      return 0;
    }

    /**
     * write the data to the inode
     * @param offset the offset from where to start writing
     * @param size the number of bytes to write
     * @param buffer where to write the data to
     * @return number of bytes written
     */
    virtual int32 writeData(uint32 /*offset*/, uint32 /*size*/, const char*/*buffer*/)
    {
      return 0;
    }

    Superblock* getSuperblock()
    {
      return superblock_;
    }

    void setSuperBlock(Superblock * sb)
    {
      superblock_ = sb;
    }

    uint32 getType()
    {
      return i_type_;
    }

    ustl::list<Dentry*>& getDentrys()
    {
      return i_dentrys_;
    }

    uint32 getNumOpenedFile()
    {
      return i_files_.size();
    }

    uint32 getSize()
    {
      return i_size_;
    }

    uint32 getMode()
    {
      return i_mode_;
    }

    int32 flush()
    {
      return 0;
    }
};
