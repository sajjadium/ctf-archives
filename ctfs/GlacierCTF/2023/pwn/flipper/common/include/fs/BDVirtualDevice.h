#pragma once

#include "types.h"
#include "ulist.h"
#include "ustring.h"

class BDDriver;
class BDRequest;

class BDDriver;
class BDRequest;

class BDVirtualDevice
{
  public:
    BDVirtualDevice(BDDriver *driver, uint32 offset, uint32 num_sectors, uint32 sector_size, const char *name,
                    bool writable);

    void addRequest(BDRequest *command);

    uint32 getBlockSize() const
    {
      return block_size_;
    }

    uint32 getDeviceNumber() const
    {
      return dev_number_;
    }

    BDDriver *getDriver()
    {
      return driver_;
    }

    const char *getName()
    {
      return name_.c_str();
    }

    uint32 getNumBlocks()
    {
      return num_sectors_ / (block_size_ / sector_size_);
    }

    /**
     * reads the data from the inode on the current device
     * @param offset where to start to read
     * @param size number of bytes that should be read
     * @param buffer to save the data that has been read
     *
     */
    virtual int32 readData(uint32 offset, uint32 size, char *buffer);

    /**
     * reads the data from the inode on the current device
     * @param offset where to start to write
     * @param size number of bytes that should be written
     * @param buffer data, that should be written
     *
     */
    virtual int32 writeData(uint32 offset, uint32 size, char *buffer);

    /**
     * the PartitionType is a 8bit field in the PartitionTable of a MBR
     * it specifies the FileSystem which is installed on the partition
     * @param part_type partition type value to be applied to the Device
     */
    void setPartitionType(uint8 part_type);

    /**
     * getting the PartitionType of this Device (value of the 8bit field
     * in Partition Table of the MBR)
     * @return the partition type
     */
    uint8 getPartitionType(void) const;

    void setDeviceNumber(uint32 number)
    {
      dev_number_ = number;
    }

    void setBlockSize(uint32 block_size)
    {
      assert(block_size % sector_size_ == 0);
      block_size_ = block_size;
    }

  private:
    BDVirtualDevice();
    uint32 dev_number_;
    uint32 offset_;
    uint32 num_sectors_;
    uint32 sector_size_;
    uint32 block_size_;
    bool writable_;
    BDDriver* driver_;
    uint8 partition_type_;
    ustl::string name_;
};

