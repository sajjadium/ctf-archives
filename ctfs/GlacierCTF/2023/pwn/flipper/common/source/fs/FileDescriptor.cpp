#include "FileDescriptor.h"
#include <ulist.h>
#ifndef EXE2MINIXFS
#include "ArchThreads.h"
#endif
#include "kprintf.h"
#include "debug.h"
#include "assert.h"
#include "Mutex.h"
#include "MutexLock.h"
#include "File.h"

FileDescriptorList global_fd_list;

static size_t fd_num_ = 3;

FileDescriptor::FileDescriptor(File* file) :
    fd_(ArchThreads::atomic_add(fd_num_, 1)),
    file_(file)
{
    debug(VFS_FILE, "Create file descriptor %u\n", getFd());
}

FileDescriptor::~FileDescriptor()
{
    assert(this);
    debug(VFS_FILE, "Destroy file descriptor %p num %u\n", this, getFd());
}

FileDescriptorList::FileDescriptorList() :
    fds_(), fd_lock_("File descriptor list lock")
{
}

FileDescriptorList::~FileDescriptorList()
{
  for(auto fd : fds_)
  {
    fd->getFile()->closeFd(fd);
  }
}

int FileDescriptorList::add(FileDescriptor* fd)
{
  debug(VFS_FILE, "FD list, add %p num %u\n", fd, fd->getFd());
  MutexLock l(fd_lock_);

  for(auto x : fds_)
  {
    if(x->getFd() == fd->getFd())
    {
      return -1;
    }
  }

  fds_.push_back(fd);

  return 0;
}

int FileDescriptorList::remove(FileDescriptor* fd)
{
  debug(VFS_FILE, "FD list, remove %p num %u\n", fd, fd->getFd());
  MutexLock l(fd_lock_);
  for(auto it = fds_.begin(); it != fds_.end(); ++it)
  {
    if((*it)->getFd() == fd->getFd())
    {
      fds_.erase(it);
      return 0;
    }
  }

  return -1;
}

FileDescriptor* FileDescriptorList::getFileDescriptor(uint32 fd_num)
{
  MutexLock l(fd_lock_);
  for(auto fd : fds_)
  {
    if(fd->getFd() == fd_num)
    {
      assert(fd->getFile());
      return fd;
    }
  }

  return nullptr;
}
