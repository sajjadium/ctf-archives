#include "fs/ramfs/RamFSInode.h"
#include "fs/ramfs/RamFSFile.h"
#include "fs/ramfs/RamFSSuperblock.h"
#include "fs/Dentry.h"

#define ERROR_FRO "ERROR: The flag muss be READONLY for several opened files"
#define ERROR_FF  "ERROR: The flag does not allow this operation"
#define ERROR_FNO "ERROR: The file is not open."

RamFSFile::RamFSFile(Inode* inode, Dentry* dentry, uint32 flag) :
    File(inode, dentry, flag)
{
  f_superblock_ = inode->getSuperblock();
  offset_ = 0;
}

RamFSFile::~RamFSFile()
{
}

int32 RamFSFile::read(char *buffer, size_t count, l_off_t offset)
{
  if (((flag_ & O_RDONLY) || (flag_ & O_RDWR)) && (f_inode_->getMode() & A_READABLE))
  {
    int32 read_bytes = f_inode_->readData(offset_ + offset, count, buffer);
    offset_ += read_bytes;
    return read_bytes;
  }
  else
  {
    // ERROR_FF
    return -1;
  }
}

int32 RamFSFile::write(const char *buffer, size_t count, l_off_t offset)
{
  if (((flag_ & O_WRONLY) || (flag_ & O_RDWR)) && (f_inode_->getMode() & A_WRITABLE))
  {
    int32 written_bytes = f_inode_->writeData(offset_ + offset, count, buffer);
    offset_ += written_bytes;
    return written_bytes;
  }
  else
  {
    // ERROR_FF
    return -1;
  }
}

int32 RamFSFile::open(uint32 __attribute__((unused)) flag)
{
  return 0;
}

int32 RamFSFile::close()
{
  return 0;
}

int32 RamFSFile::flush()
{
  return 0;
}
