#include "MinixFSFile.h"
#include "MinixFSInode.h"
#include "Inode.h"

MinixFSFile::MinixFSFile(Inode* inode, Dentry* dentry, uint32 flag) :
    File(inode, dentry, flag)
{
  f_superblock_ = inode->getSuperblock();
  offset_ = 0;
}

MinixFSFile::~MinixFSFile()
{
}

int32 MinixFSFile::read(char *buffer, size_t count, l_off_t offset)
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

int32 MinixFSFile::write(const char *buffer, size_t count, l_off_t offset)
{
  if (((flag_ & O_WRONLY) || (flag_ & O_RDWR)) && (f_inode_->getMode() & A_WRITABLE))
  {
    int32 written = f_inode_->writeData(offset_ + offset, count, buffer);
    offset_ += written;
    return written;
  }
  else
  {
    // ERROR_FF
    return -1;
  }
}

int32 MinixFSFile::flush()
{
  ((MinixFSInode *) f_inode_)->flush();
  return 0;
}

