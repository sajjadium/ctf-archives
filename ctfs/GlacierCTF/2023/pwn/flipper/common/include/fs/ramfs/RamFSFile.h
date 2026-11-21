#pragma once

#include "fs/File.h"


class RamFSFile: public File
{
  public:

    RamFSFile ( Inode* inode, Dentry* dentry, uint32 flag );

    virtual ~RamFSFile();

    /**
     * Sets the file position relative to the start of the file, the  end of
     * the file or the current file position.
     * @param offset is the offset to set.
     * @param origin is the on off SEEK_SET, SEEK_CUR and SEEK_END.
     * @return the offset from the start off the file or -1 on failure.
     */
    l_off_t llSeek ( l_off_t offset, uint8 origin );


    /**
     * reads from the file
     * @param buffer is the buffer where the data is written to
     * @param count is the number of bytes to read.
     * @param offset is the offset to read from counted from the start of the file.
     * @return the number of bytes read
     */
    virtual int32 read ( char *buffer, size_t count, l_off_t offset );

    /**
     * writes to the file
     * @param buffer is the buffer where the data is read from
     * @param count is the number of bytes to write.
     * @param offset is the offset to write from counted from the start of the file.
     * @return the number of bytes written
     */
    virtual int32 write ( const char *buffer, size_t count, l_off_t offset );

    /**
     * Opens the file
     * @param flag how to open the file
     * @return the filedescriptor
     */
    virtual int32 open ( uint32 flag );

    /**
     * Closes the file
     * @return 0 on success
     */
    virtual int32 close();

    /**
     * Flushes all off the file's write operations. The File will be written to disk.
     * @return is the error code of the flush operation.
     */
    virtual int32 flush();
};

