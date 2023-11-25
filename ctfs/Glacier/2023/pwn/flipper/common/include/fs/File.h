#pragma once

#include "types.h"
#include "ulist.h"

class Superblock;
class Inode;
class Dentry;
class FileDescriptor;

#define O_RDONLY    0x0001
#define O_WRONLY    0x0002
#define O_RDWR      0x0004
#define O_CREAT     0x0008
#define O_APPEND    0x0010
#define O_EXCL      0x0020
#define O_NONBLOCK  0x0040
#define O_TRUNC     0x0080
#define O_SYNC      0x0100
#define O_DSYNC     0x0200
#define O_RSYNC     O_SYNC

#ifndef SEEK_SET
#define SEEK_SET 0
#endif
#ifndef SEEK_CUR
#define SEEK_CUR 1
#endif
#ifndef SEEK_END
#define SEEK_END 2
#endif


class File
{
  public:
    uint32 uid;
    uint32 gid;

    /**
     * interna version number.
     */
    uint32 version;

  protected:

    /**
     * The superblock  pointing to this file
     */
    Superblock* f_superblock_;

    /**
     * The inode associated to the file.
     */
    Inode* f_inode_;

    /**
     * The dentry pointing to this file/
     */
    Dentry* f_dentry_;

    /**
     * The flags specified when the file was opened
     */
    uint32 flag_;


    /**
     * Current offset in the file
     */
    l_off_t offset_;

    /**
     * List of open file descriptors
     */
    ustl::list<FileDescriptor*> f_fds_;

  public:
    /**
     * returns the files flag
     * @return the flag
     */
    uint32 getFlag()
    {
      return flag_;
    }

  public:

    /**
     * The Constructor
     * @param inode the files inode
     * @param dentry the files dentry
     * @param flag the files flag
     */
    File(Inode* inode, Dentry* dentry, uint32 flag);

    virtual ~File();

    virtual FileDescriptor* openFd();
    virtual int closeFd(FileDescriptor* fd);



    Dentry* getDentry()
    {
      return f_dentry_;
    }
    Inode* getInode()
    {
      return f_inode_;
    }

    /**
     * Sets the file position relative to the start of the file, the end of the
     * file or the current file position.
     * @param offset is the offset to set.
     * @param origin is the on off SEEK_SET, SEEK_CUR and SEEK_END.
     * @returns the offset from the start off the file or -1 on failure.
     */
    l_off_t lseek(l_off_t offset, uint8 origin);

    /**
     * not implemented here
     * reads from the file
     * @param buffer is the buffer where the data is written to
     * @param count is the number of bytes to read.
     * @param offset is the offset to read from counted from the current file position.
     */
    virtual int32 read(char */*buffer*/, size_t /*count*/, l_off_t /*offset*/)
    {
      return 0;
    }

    /**
     * not implemented here
     * write to the file
     * @param buffer is the buffer where the data is read from
     * @param count is the number of bytes to write.
     * @param offset is the offset to write from counted from the current file position
     */
    virtual int32 write(const char */*buffer*/, size_t /*count*/, l_off_t /*offset*/)
    {
      return 0;
    }

    /**
     * Opens the file
     * @param inode is the inode the read the file from.
     */
    virtual int32 open(uint32)
    {
      return 0;
    }

    /**
     * not implemented here
     * Close the file
     * @param inode is close, the superblock has the information, that this
     * inode is not use anymore.
     */
    virtual int32 close()
    {
      return 0;
    }

    /**
     * not implemented here
     * Flush all off the file's write operations. The File will be written to disk.
     * @return is the error code of the flush operation.
     */
    virtual int32 flush()
    {
      return 0;
    }

    virtual uint32 getSize();
};
