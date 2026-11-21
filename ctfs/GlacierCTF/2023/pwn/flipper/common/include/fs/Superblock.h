#pragma once

#include "types.h"
#include <ulist.h>

class Iattr;
class Statfs;
class WaitQueue;
class FileSystemType;
class VirtualFileSystem;
class FileDescriptor;

class Dentry;
class Inode;
class File;

class Superblock
{
  public:

    friend class VirtualFileSystem;

    /**
     * This records an identification number that has been read from the device
     * to confirm that the data on the device corresponds to the file-system
     */
    uint64 s_magic_;

  protected:

    const FileSystemType *s_type_;

    /**
     * The device that this file-system is mounted on.
     */
    size_t s_dev_;

    /**
     * This is a list of flags which are logically with the flags in each
     * inode to detemine certain behaviours. There is one flag which applies
     * only to the whole file-system.
     * exp: MS_RDONLY
     * A file-system with the flag set has been mounted read-only. No writing
     * be permitted, and no indirect modification, such as mount time in the
     * super-block or access times on files, will be made.
     */
    uint64 s_flags_;

    /**
     * The Dentry refers the root of the file-system. It is normally created by
     * loading the root inode from the file-system.
     */
    Dentry *s_root_;

    /**
     * The old Dentry of the mount point of a mounted file system
     */
    Dentry *s_mountpoint_;

    /**
     * A list of dirty inodes.
     */
    ustl::list<Inode*> dirty_inodes_;

    /**
     * A list of used inodes. It is only used to open-file.
     */
    ustl::list<Inode*> used_inodes_;

    /**
     * inodes of the superblock.
     */
    ustl::list<Inode*> all_inodes_;

    /**
     * This is a list of files (linked on f_list) of open files on this
     * file-system. It is used, for example, to check if there are any files
     * open for write before remounting the file-system as read-only.
     */
    ustl::list<File*> s_files_;


  public:

    /**
     * constructor
     * @param s_dev the device number of the new filesystem
     */
    Superblock(FileSystemType* fs_type, size_t s_dev);

    virtual ~Superblock();

    /**
     * create a new Inode of the superblock
     * @param dentry the dentry to create the inode with
     * @param type the inode type
     * @return the created inode
     */
    virtual Inode* createInode(uint32 type) = 0;

    /**
     * This method is called to read a specific inode from a mounted
     * file-system.
     * @param inode the inode to read
     * @return 0 on success
     */
    virtual int32 readInode(Inode* /*inode*/)
    {
      return 0;
    }

    /**
     * This method is called to write a specific inode to a mounted file-system,
     * and gets called on inodes which have been marked dirty.
     * @param inode the inode to write
     */
    virtual void writeInode(Inode* /*inode*/)
    {
    }

    /**
     * This method is called whenever the reference count on an inode reaches 0,
     * and it is found that the link count (i_nlink= is also zero. It si
     * presumed that the file-system will deal with this situation be
     * invalidating the inode in the file-system and freeing up any resourses
     * used.
     * @param inode the inode to delete
     */
    virtual void deleteInode(Inode* /*inode*/);


    virtual int fileOpened(File* file);
    virtual int fileReleased(File* file);

    virtual void releaseAllOpenFiles();
    virtual void deleteAllInodes();

    /**
     * Get the root Dentry of the Superblock
     * @return the root dentry
     */
    Dentry *getRoot();

    /**
     * Get the mount point Dentry of the Superblock
     * @return the superblocks mount point dentry
     */
    Dentry *getMountPoint();

    /**
     * Set the mount point Dentry of the Superblock
     */
    void setMountPoint(Dentry* mountpoint);

    /**
     * Get the File System Type of the Superblock
     * @return the file system type
     */
    FileSystemType *getFSType();
};


