#pragma once

#include "types.h"

class Dirent;
class Dentry;
class VfsMount;
class FileDescriptor;
class VfsSyscall;
class Path;
class FileSystemInfo;

class VfsSyscall
{
  public:

    /**
     * make a new directory.
     * i.e. im the path "/file/test/" create a new directory with the name
     * "dir". => the new_dir ist "/file/test/dir"
     * @param pathname the new directory.
     * @param type the permission.
     * @return On success, zero is returned. On error, -1 is returned.
     */
    static int32 mkdir(const char* pathname, int32 /*type*/);

    /**
     * The readdir() displays or saves the names from all childs into buffer and returns a pointer
     * to a Dirent.
     * @param pathname the destination-directory.
     * @param buffer the buffer the output is saved to
     * @param size the size of buffer in bytes
     * @return the dirent
     */
    static Dirent* readdir(const char* pathname, char* buffer = 0, size_t size = 0);

    /**
     * chdir() changes the current directory to the specified directory.
     * @param dir the destination-directory.
     * @return On success, zero is returned. On error, -1 is returned.
     */
    static int32 chdir(const char* pathname);

    /**
     * delete a directory, which must be empty.
     * @param pathname the removed directory
     * @return On success, zero is returned. On error, -1 is returned.
     */
    static int32 rmdir(const char* pathname);

    /**
     * remove a directory (which must be empty) or a file
     * @param pathname the removed directory or file
     * @return On success, zero is returned. On error, -1 is returned.
     */
    static int32 rm(const char* pathname);

    /**
     * The open() is used to convert a pathname into a file descriptor, if the
     * pathname does not exist, create a new file.
     * @param pathname the file pathname
     * @param flag specified when the file was opened
     * @return On success, file descriptor is returned. On error, -1 is returned.
     */
    static int32 open(const char* pathname, uint32 flag);

    /**
     * The close() closes a file descriptor.
     * @param fd the file descriptor
     * @return On success, zero is returned. On error, -1 is returned.
     */
    static int32 close(uint32 fd);

    /**
     * The read() attempts to read up to count bytes from file descriptor fd
     * into the buffer starting at buffter.
     * @param fd the file descriptor
     * @param buffer the buffer that to read the date
     * @param count the size of the byte
     * @return On success, the number of bytes read is returned (zero indicates
     *         end of file), and the file position is advanced by this number.
     *         On error, -1 is returned.
     */
    static int32 read(uint32 fd, char* buffer, uint32 count);

    /**
     * Sets the file position relative to the start of the file, the end of the
     * file or the current file position.
     * @param fd the file descriptor
     * @param offset is the offset to set.
     * @param origin is the on off SEEK_SET, SEEK_CUR and SEEK_END.
     * @returns the offset from the start off the file or -1 on failure.
     */
    static l_off_t lseek(uint32 fd, l_off_t offset, uint8 origin);

    /**
     * write  writes  up  to  count  bytes  to the file referenced by the file
     * descriptor fd from the buffer starting at buf.
     * @param fd the file descriptor
     * @param buffer the buffer that to store the date
     * @param count the size of the byte
     * @return On success, the number of bytes written are returned (zero
     *         indicates nothing was written). On error, -1 is returned
     */
    static int32 write(uint32 fd, const char *buffer, uint32 count);

    /**
     * flushes the file with the given file descriptor to the disc
     * so that changes in the system are written to disc
     * @param fd the file descriptor
     * @return 0 on success, -1 on error
     */
    static int32 flush(uint32 fd);

    /**
     * mounts a file system
     * @param device_name the device name i.e. ida
     * @param dir_name the directory name where to mount the filesystem
     * @param file_system_name the file system name i.e. minixfs
     * @param flag the flag indicates if mounted readonly etc.
     * @return 0 on success
     */
    static int32 mount(const char *device_name, const char *dir_name, const char *file_system_name, int32 flag);

    /** unmounts a filesystem
     * @param dir_name the directory where the filesystem to unmount is mounted
     * @param flag not used
     * @return 0 on success
     */
    static int32 umount(const char *dir_name, int32 flag);

    /**
     * returns the size of a file
     * @param fd the file looking for
     * @return the size
     */
    static uint32 getFileSize(uint32 fd);

    /**
     * get the File descriptor object from the global variable
     * @param the fd int
     * @return the file descriptor object
     */
    static FileDescriptor* getFileDescriptor(uint32 fd);

  private:
    VfsSyscall();
    ~VfsSyscall();
};

