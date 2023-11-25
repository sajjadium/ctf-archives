#include "fs/devicefs/DeviceFSSuperblock.h"
#include "fs/ramfs/RamFSInode.h"
#include "DeviceFSType.h"
#include "fs/Dentry.h"
#include "fs/Inode.h"
#include "fs/File.h"
#include "fs/FileDescriptor.h"

#include "console/kprintf.h"

#include "Console.h"

class DeviceFSType;

extern Console* main_console;

const char DeviceFSSuperBlock::ROOT_NAME[] = "/";
const char DeviceFSSuperBlock::DEVICE_ROOT_NAME[] = "dev";

DeviceFSSuperBlock* DeviceFSSuperBlock::instance_ = 0;

DeviceFSSuperBlock::DeviceFSSuperBlock(DeviceFSType* fs_type, uint32 s_dev) :
    RamFSSuperblock(fs_type, s_dev)
{
}

DeviceFSSuperBlock::~DeviceFSSuperBlock()
{
}

void DeviceFSSuperBlock::addDevice(Inode* device_inode, const char* node_name)
{
  // Devices are mounted at the devicefs root (s_root_)
  device_inode->setSuperBlock(this);

  Dentry* fdntr = new Dentry(device_inode, s_root_, node_name);

  assert(device_inode->mknod(fdntr) == 0);
  all_inodes_.push_back(device_inode);
}

DeviceFSSuperBlock* DeviceFSSuperBlock::getInstance()
{
    if (!instance_)
        instance_ = new DeviceFSSuperBlock(DeviceFSType::getInstance(), 0);
    return instance_;
}
