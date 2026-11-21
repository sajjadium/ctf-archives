#include "Superblock.h"
#include "assert.h"
#include "Dentry.h"
#include "Inode.h"
#include "File.h"
#include "FileSystemType.h"

Superblock::Superblock(FileSystemType* fs_type, size_t s_dev) :
    s_magic_(0), s_type_(fs_type), s_dev_(s_dev), s_flags_(0), s_root_(0), s_mountpoint_(0)
{
    debug(SUPERBLOCK, "%s Superblock created\n", s_type_->getFSName());
}

Superblock::~Superblock()
{
    debug(SUPERBLOCK, "%s Superblock destroyed\n", s_type_->getFSName());
}

void Superblock::deleteInode(Inode* inode)
{
  assert(inode != 0);
  dirty_inodes_.remove(inode);
  used_inodes_.remove(inode);
  all_inodes_.remove(inode);
  delete inode;
}

Dentry* Superblock::getRoot()
{
  return s_root_;
}

Dentry* Superblock::getMountPoint()
{
  return s_mountpoint_;
}

void Superblock::setMountPoint(Dentry* mountpoint)
{
    s_mountpoint_ = mountpoint;
}

FileSystemType* Superblock::getFSType()
{
  return (FileSystemType*) s_type_;
}


int Superblock::fileOpened(File* file)
{
    Inode* inode = file->getInode();
    assert(inode->getSuperblock() == this);

    if(ustl::find(s_files_.begin(), s_files_.end(), file) != s_files_.end())
    {
        return -1;
    }

    s_files_.push_back(file);
    used_inodes_.push_back(inode);

    return 0;
}

int Superblock::fileReleased(File* file)
{
    Inode* inode = file->getInode();
    assert(inode->getSuperblock() == this);

    s_files_.remove(file);

    if (inode->getNumOpenedFile() == 0)
    {
        used_inodes_.remove(inode);
    }

    return 0;
}

void Superblock::releaseAllOpenFiles()
{
    debug(SUPERBLOCK, "Releasing all open files\n");
    while(!s_files_.empty())
    {
        File* file = s_files_.front();
        file->getInode()->release(file);
    }

    assert(s_files_.empty());
}

void Superblock::deleteAllInodes()
{
    for (Inode* inode : all_inodes_)
    {
        while(!inode->getDentrys().empty())
        {
            delete inode->getDentrys().front();
        }

        debug(SUPERBLOCK, "~Superblock write inode to disc\n");
        writeInode(inode);

        debug(SUPERBLOCK, "~Superblock delete inode %p\n", inode);
        delete inode;
    }

    all_inodes_.clear();
}
