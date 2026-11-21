#pragma once

#include "types.h"
#include <ustl/ulist.h>

/**
 * File system flag indicating if the system in question requires an device.
 */
#define FS_REQUIRES_DEV   0x0001 // located on a physical disk device
#define FS_NOMOUNT        0x0010 // Filesystem has no mount point

/**
 * The maximal number of file system types.
 */
#define MAX_FILE_SYSTEM_TYPES 16

class Superblock;
class FileSystemType;
class VfsMount;
class Dentry;
class FileSystemInfo;

class VirtualFileSystem
{
  protected:
    ustl::list<Superblock*> superblocks_;
    ustl::list<VfsMount*> mounts_;
    ustl::list<FileSystemType*> file_system_types_;

  public:
    void initialize();
    VirtualFileSystem();
    ~VirtualFileSystem();

    /**
     * register the file-system-type to the vfs
     * @param file_system_type the file system type to register
     * @return 0 on success, -1 if a file-system-type with that name has
     * already been registered
     */
    int32 registerFileSystem(FileSystemType *file_system_type);

    /**
     * unregister the file-system-typt to the vfs
     * @param file_system_type the file system type to unregister
     * @return 0 on success
     */
    int32 unregisterFileSystem(FileSystemType *file_system_type);

    /**
     * The getFsType function receives a filesystem name as its parameter, scans
     * the list of registered filesystems looking at the fs_name field of their
     * descriptors, and returns a pointer to the corresponding FileSystemType
     * object, if is present.
     * @param fs_name the name of the filesystem
     * @return the file system type
     */
    FileSystemType *getFsType(const char* fs_name);

    /**
     * found the VfsMount from mounts_ list with given dentry.
     * @param dentry the mount-point-dentry or root-dentry
     * @param is_mount_point if it is false, check with root-dentry,
     *         else mount-point-dentry
     */
    VfsMount *getVfsMount(const Dentry* dentry, bool is_root = false);

    /**
     * mount the dev_name (device name) to the directory specified by dir_name.
     * @param dev_name the device file name of the block device storing the
     *                  filesystem. Shall be a empty string to mount pseudo
     *                  file sytems.
     * @param dir_name the mount pointer directory
     * @param fs_name the name of the type of filesystem to be mounted
     * @param flags the mount flags
     * @param data contain arbitray fs-dependent information (or be NULL)
     * @return On success, zero is returned. On error, -1 is returned.
     */
    int32 mount(const char* dev_name, const char* dir_name, const char* fs_name, uint32 flags/*, void *data*/);

    /**
     * unmount the filesystem
     * @param dir_name the mount pointer direcotry or (block devie block filename)
     * @param flags the umount flags
     * @return On success, zero is returned. On error, -1 is returned.
     */
    int32 umount(const char* dir_name, uint32 flags);

    /**
     * mount the ROOT to the VFS. (special of the mount)
     * @param fs_name the name of the type of filesystem to be mounted
     * @param flags the mount flags
     * @return On success, zero is returned. On error, -1 is returned.
     */
    FileSystemInfo *rootMount(const char* fs_name, uint32 flags);

    /**
     * umount the ROOT from the VFS (special of the umount)
     * @return On success, zero is returned. On error, -1 is returned.
     */
    int32 rootUmount();

};

extern VirtualFileSystem vfs;

