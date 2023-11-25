#pragma once

#include "ustring.h"
#include "FiFo.h"

class CharacterDevice
{
  public:

    /**
     * Constructor
     * @param name the device name
     * @param super_block the superblock (0)
     * @param inode_type the inode type (cahracter device)
     */
    CharacterDevice(const char* name) :
        in_buffer_(CD_BUFFER_SIZE, FIFO_NOBLOCK_PUT | FIFO_NOBLOCK_PUT_OVERWRITE_OLD),
        out_buffer_(CD_BUFFER_SIZE, FIFO_NOBLOCK_PUT | FIFO_NOBLOCK_PUT_OVERWRITE_OLD),
        name_(name)
    {
    }

    ~CharacterDevice()
    {
    }

    /**
     * reads the data from the character device
     * @param buffer is the buffer where the data is written to
     * @param count is the number of bytes to read.
     * @param offset is never to be used, because there is no offset
     *        in character devices, but it is defined in the Inode interface
     */
    virtual int32 readData(uint32 offset, uint32 size, char *buffer)
    {
      if (offset)
        return -1; // offset reading not supprted with char devices

      char *bptr = buffer;
      do
      {
        *bptr++ = in_buffer_.get();
      } while ((bptr - buffer) < (int32) size);

      return (bptr - buffer);
    }

    /**
     * writes to the character device
     * @param buffer is the buffer where the data is read from
     * @param count is the number of bytes to write.
     * @param offset is never to be used, because there is no offset
     *        in character devices, but it is defined in the Inode interface
     */
    virtual int32 writeData(uint32 offset, uint32 size, const char*buffer)
    {
      if (offset)
        return -1; // offset writing also not supp0rted

      const char *bptr = buffer;
      do
      {
        out_buffer_.put(*bptr++);
      } while ((bptr - buffer) < (int32) size);

      return (bptr - buffer);
    }

    const char *getDeviceName() const
    {
      return name_.c_str();
    }

  protected:
    static const uint32 CD_BUFFER_SIZE = 1024;

    FiFo<uint8> in_buffer_;
    FiFo<uint8> out_buffer_;

    ustl::string name_;

    void processInBuffer()
    {
      in_buffer_.get();
    }

    void processOutBuffer()
    {
      out_buffer_.get();
    }

};


