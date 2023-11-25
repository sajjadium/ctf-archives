#include "File.h"
#include "Inode.h"
#include "FileDescriptor.h"
#include "assert.h"
#include "Superblock.h"
#include "FileSystemType.h"


File::File(Inode* inode, Dentry* dentry, uint32 flag) :
    uid(0), gid(0), version(0), f_superblock_(0), f_inode_(inode), f_dentry_(dentry), flag_(flag)
{
    f_inode_->incRefCount();
}

File::~File()
{
  debug(VFS_FILE, "Destroying file\n");

  assert(f_fds_.empty() && "File to be destroyed still has open file descriptors");
  assert(f_inode_);

  if(!f_inode_->decRefCount())
  {
      debug(VFS_FILE, "No more references to %s inode %p left after closing file, deleting\n",
            f_inode_->getSuperblock()->getFSType()->getFSName(), f_inode_);
    f_inode_->getSuperblock()->deleteInode(f_inode_);
  }
}

uint32 File::getSize()
{
  return f_inode_->getSize();
}

l_off_t File::lseek(l_off_t offset, uint8 origin)
{
  if (origin == SEEK_SET)
    offset_ = offset;
  else if (origin == SEEK_CUR)
    offset_ += offset;
  else if (origin == SEEK_END)
    offset_ = f_inode_->getSize() + offset;
  else
    return -1;

  return offset_;
}




FileDescriptor* File::openFd()
{
    debug(VFS_FILE, "Open new file descriptor\n");
    FileDescriptor* fd = new FileDescriptor(this);
    f_fds_.push_back(fd);

    debug(VFS_FILE, "New file descriptor num: %u\n", fd->getFd());
    return fd;
}


int File::closeFd(FileDescriptor* fd)
{
    debug(VFS_FILE, "Close file descriptor num %u\n", fd->getFd());
    assert(fd);

    f_fds_.remove(fd);
    delete fd;

    // Release on last fd removed
    if(f_fds_.empty())
    {
        debug(VFS_FILE, "Releasing file\n");
        return getInode()->release(this); // Will delete this file object
    }

    return 0;
}
