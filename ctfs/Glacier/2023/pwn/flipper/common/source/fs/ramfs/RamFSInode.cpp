#include "fs/ramfs/RamFSInode.h"
#include "kstring.h"
#include "assert.h"
#include "fs/ramfs/RamFSSuperblock.h"
#include "fs/ramfs/RamFSFile.h"
#include "fs/Dentry.h"
#include "FileSystemType.h"

#include "console/kprintf.h"

#define BASIC_ALLOC 256

RamFSInode::RamFSInode(Superblock *super_block, uint32 inode_type) :
    Inode(super_block, inode_type),
    data_(0)
{
  debug(RAMFS, "New RamFSInode %p\n", this);
  if (inode_type == I_FILE)
  {
    data_ = new char[BASIC_ALLOC]();
    i_size_ = BASIC_ALLOC;
  }
}

RamFSInode::~RamFSInode()
{
  debug(RAMFS, "Destroying RamFSInode %p\n", this);
  delete[] data_;
}

int32 RamFSInode::readData(uint32 offset, uint32 size, char *buffer)
{
  if(offset >= getSize())
  {
    return 0;
  }

  uint32 read_size = Min(size, getSize() - offset);

  char *ptr_offset = data_ + offset;
  memcpy(buffer, ptr_offset, read_size);
  return read_size;
}

int32 RamFSInode::writeData(uint32 offset, uint32 size, const char *buffer)
{
  assert(i_type_ == I_FILE);

  if(offset >= getSize())
  {
    return 0;
  }

  uint32 write_size = Min(size, getSize() - offset);
  if(write_size != size)
  {
    debug(RAMFS, "WARNING: RamFS currently does not support expanding files via the write syscall\n");
  }

  char *ptr_offset = data_ + offset;
  memcpy(ptr_offset, buffer, write_size);
  return write_size;
}

File* RamFSInode::open(Dentry* dentry, uint32 flag)
{
  debug(INODE, "%s Inode: Open file\n", getSuperblock()->getFSType()->getFSName());
  assert(ustl::find(i_dentrys_.begin(), i_dentrys_.end(), dentry) != i_dentrys_.end());

  File* file = (File*) (new RamFSFile(this, dentry, flag));
  i_files_.push_back(file);
  getSuperblock()->fileOpened(file);
  return file;
}
