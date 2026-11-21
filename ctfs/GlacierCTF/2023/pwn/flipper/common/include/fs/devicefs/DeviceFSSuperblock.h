#pragma once

#include "fs/Superblock.h"
#include "fs/ramfs/RamFSSuperblock.h"

class Inode;
class Superblock;
class CharacterDevice;
class DeviceFSType;

class DeviceFSSuperBlock : public RamFSSuperblock
{
  public:
    static const char ROOT_NAME[];
    static const char DEVICE_ROOT_NAME[];

    virtual ~DeviceFSSuperBlock();

    /**
     * addsa new device to the superblock
     * @param inode the inode of the device to add
     * @param node_name the device name
     */
    void addDevice(Inode* inode, const char* node_name);

    /**
     * Access method to the singleton instance
     */
    static DeviceFSSuperBlock* getInstance();

  private:

    /**
     * Constructor
     * @param s_root the root Dentry of the new Filesystem
     * @param s_dev the device number of the new Filesystem
     */
    DeviceFSSuperBlock(DeviceFSType* fs_type, uint32 s_dev);

  protected:
    static DeviceFSSuperBlock* instance_;

};

