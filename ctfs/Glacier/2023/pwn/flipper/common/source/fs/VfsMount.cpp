#include "VfsMount.h"


VfsMount::VfsMount() :
    mnt_parent_ ( 0 ),
    mnt_mountpoint_ ( 0 ),
    mnt_root_ ( 0 ),
    mnt_sb_ ( 0 ),
    mnt_flags_ ( 0 )
{}


VfsMount::VfsMount ( VfsMount* parent, Dentry * mountpoint, Dentry* root,
                     Superblock* superblock, int32 flags ) :
    mnt_parent_ ( parent ? parent : this),
    mnt_mountpoint_ ( mountpoint ),
    mnt_root_ ( root ),
    mnt_sb_ ( superblock ),
    mnt_flags_ ( flags )
{}


VfsMount::~VfsMount()
{
  mnt_parent_ = 0;
  mnt_mountpoint_ = 0;
  mnt_root_ = 0;
  mnt_sb_ = 0;
  mnt_flags_ = 0;
}


VfsMount *VfsMount::getParent() const
{
  return mnt_parent_;
}


Dentry *VfsMount::getMountPoint() const
{
  return mnt_mountpoint_;
}


Dentry *VfsMount::getRoot() const
{
  return mnt_root_;
}


Superblock *VfsMount::getSuperblock() const
{
  return mnt_sb_;
}


int32 VfsMount::getFlags() const
{
  return mnt_flags_;
}


//NOTE: only used as workaround
void VfsMount::clear()
{
  mnt_parent_ = 0;
  mnt_mountpoint_ = 0;
  mnt_root_ = 0;
  mnt_sb_ = 0;
  mnt_flags_ = 0;
}


bool VfsMount::isRootMount() const
{
    return getParent() == this;
}
