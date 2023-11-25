#pragma once

#include "types.h"

class Superblock;
class Dentry;

#define FS_REQUIRES_DEV   0x0001 // located on a physical disk device
#define FS_NOMOUNT        0x0010 // Filesystem has no mount point

#define MAX_FILE_SYSTEM_TYPES 16

class FileSystemType
{

  protected:
    const char *fs_name_;
    int32 fs_flags_;

  public:
    FileSystemType(const char *fs_name);
    virtual ~FileSystemType();

    FileSystemType const &operator =(FileSystemType const &instance)
    {
      fs_name_ = instance.fs_name_;
      fs_flags_ = instance.fs_flags_;
      return (*this);
    }

    const char* getFSName() const;
    void setFSName(const char* fs_name);
    int32 getFSFlags() const;
    void setFSFlags(int32 fs_flags);

    /**
     * Reads the superblock from the device.
     * @param superblock is the superblock to fill with data.
     * @param data is the data given to the mount system call.
     * @return is a pointer to the resulting superblock.
     */
    virtual Superblock *readSuper(Superblock *superblock, void *data) const = 0;

    /**
     * Creates an Superblock object for the actual file system type.
     * @param s_dev a valid device number or -1 if no block device is available
     *              (e.g. for pseudo file systems)
     * @return a pointer to the Superblock object, 0 if wasn't possible to
     * create a Superblock with the given device number
     */
    virtual Superblock *createSuper(uint32 s_dev) = 0;

};

