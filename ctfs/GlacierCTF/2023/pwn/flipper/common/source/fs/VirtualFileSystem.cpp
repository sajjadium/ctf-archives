#include "FileSystemType.h"
#include "FileSystemInfo.h"
#include "PathWalker.h"
#include "VirtualFileSystem.h"
#include "Dentry.h"
#include "Superblock.h"
#include "VfsMount.h"
#include "kstring.h"
#include "assert.h"
#include "BDManager.h"
#include "BDVirtualDevice.h"
#include "Thread.h"

#include "console/kprintf.h"

VirtualFileSystem vfs;

void VirtualFileSystem::initialize()
{
  new (this) VirtualFileSystem();
}

VirtualFileSystem::VirtualFileSystem()
{
}

VirtualFileSystem::~VirtualFileSystem()
{
}

int32 VirtualFileSystem::registerFileSystem(FileSystemType *file_system_type)
{
  assert(file_system_type);
  assert(file_system_type->getFSName());

  // check whether a file system type with that name has already been
  // registered
  if (getFsType(file_system_type->getFSName()))
    return -1;
  file_system_types_.push_back(file_system_type);
  return 0;
}

int32 VirtualFileSystem::unregisterFileSystem(FileSystemType *file_system_type)
{
  assert(file_system_type != 0);

  const char *fs_name = file_system_type->getFSName();
  for (FileSystemType* fst : file_system_types_)
  {
    if (strcmp(fst->getFSName(), fs_name) == 0)
      delete fst;
  }
  return 0;
}

FileSystemType *VirtualFileSystem::getFsType(const char* fs_name)
{
  assert(fs_name);

  for (FileSystemType* fst : file_system_types_)
  {
    if (strcmp(fst->getFSName(), fs_name) == 0)
      return fst;
  }
  return 0;
}

VfsMount *VirtualFileSystem::getVfsMount(const Dentry* dentry, bool is_root)
{
  assert(dentry);

  if (is_root == false)
  {
    for (VfsMount* mnt : mounts_)
    {
      debug(VFS, "getVfsMount> mnt->getMountPoint()->getName() : %s\n", mnt->getMountPoint()->getName());
      if (!is_root && (mnt->getMountPoint()) == dentry)
        return mnt;
      else if (mnt->getRoot() == dentry)
        return mnt;
    }
  }
  return 0;
}

FileSystemInfo *VirtualFileSystem::rootMount(const char *fs_name, uint32 /*flags*/)
{
  FileSystemType *fst = getFsType(fs_name);
  if(!fst)
  {
      debug(VFS, "Unknown file system %s\n", fs_name);
      return nullptr;
  }

  if(fst->getFSFlags() & FS_REQUIRES_DEV)
  {
      debug(VFS, "Only file systems that do not require a device are currently supported as root file system\n");
      return nullptr;
  }

  debug(VFS, "Create root %s superblock\n", fst->getFSName());
  Superblock *super = fst->createSuper(-1);
  super = fst->readSuper(super, 0);

  Dentry *root = super->getRoot();

  super->setMountPoint(root);
  root->setMountedRoot(root);

  VfsMount *root_mount = new VfsMount(0, root, root, super, 0);

  mounts_.push_back(root_mount);
  superblocks_.push_back(super);

  // fs_info initialize
  FileSystemInfo *fs_info = new FileSystemInfo();
  Path root_path(root, root_mount);
  fs_info->setRoot(root_path);
  fs_info->setPwd(root_path);

  assert(root_mount->getParent() == root_mount);
  assert(root_mount->getMountPoint() == root);
  assert(root->getParent() == root);
  assert(root->getMountedRoot() == root);
  assert(super->getMountPoint() == super->getRoot());

  return fs_info;
}

int32 VirtualFileSystem::mount(const char* dev_name, const char* dir_name, const char* fs_name, uint32 /*flags*/)
{
  debug(VFS, "Mount fs %s at %s with device %s\n", fs_name, dir_name, dev_name ? dev_name : "(null)");

  if ((!dir_name) || (!fs_name))
      return -1;

  FileSystemType *fst = getFsType(fs_name);
  if (!fst)
      return -1;

  if ((fst->getFSFlags() & FS_REQUIRES_DEV) && !dev_name)
      return -1;

  FileSystemInfo *fs_info = currentThread->getWorkingDirInfo();
  assert(fs_info);

  uint32_t dev = -1;
  if(fst->getFSFlags() & FS_REQUIRES_DEV)
  {
      BDVirtualDevice* bddev = BDManager::getInstance()->getDeviceByName(dev_name);
      if (!bddev)
      {
          debug(VFS, "mount: device with name %s doesn't exist\n", dev_name);
          return -1;
      }

      dev = bddev->getDeviceNumber();
      debug(VFS, "mount: dev_nr: %d\n", dev);
  }

  // Find mount point
  Path mountpoint_path;
  int32 success = PathWalker::pathWalk(dir_name, fs_info->getPwd(), fs_info->getRoot(), mountpoint_path);

  if (success != 0)
  {
      debug(VFS, "mount: Could not find mountpoint\n");
      return -1;
  }

  // create a new superblock
  debug(VFS, "Create %s superblock\n", fst->getFSName());
  Superblock *super = fst->createSuper(dev);
  if (!super)
  {
      debug(VFS, "mount: Superblock creation failed\n");
      return -1;
  }

  debug(VFS, "mount: Fill superblock\n");
  super = fst->readSuper(super, 0); //?

  Dentry *root = super->getRoot();
  assert(root->getParent() == root);

  super->setMountPoint(mountpoint_path.dentry_); // Set mountpoint for new superblock
  mountpoint_path.dentry_->setMountedRoot(root);  // Mountpoint mounts new superblock root

  // create a new vfs_mount
  VfsMount* new_mount = new VfsMount(mountpoint_path.mnt_, mountpoint_path.dentry_, root, super, 0);
  mounts_.push_back(new_mount);
  superblocks_.push_back(super);

  assert(new_mount->getParent() == mountpoint_path.mnt_);
  assert(new_mount->getMountPoint() == mountpoint_path.dentry_);
  assert(new_mount->getSuperblock() == super);
  assert(new_mount->getRoot() == root);

  return 0;
}

int32 VirtualFileSystem::rootUmount()
{
  if (superblocks_.size() == 0)
  {
    return -1;
  }
  VfsMount *root_vfs_mount = mounts_.at(0);
  delete root_vfs_mount;

  Superblock *root_sb = superblocks_.at(0);
  delete root_sb;
  return 0;
}

int32 VirtualFileSystem::umount(const char* dir_name, uint32 /*flags*/)
{
  FileSystemInfo *fs_info = currentThread->getWorkingDirInfo();
  if (dir_name == 0)
    return -1;

  Path mountpount_path;
  int32 success = PathWalker::pathWalk(dir_name, fs_info->getPwd(), fs_info->getRoot(), mountpount_path);

  if (success != 0)
  {
      debug(VFS, "(umount) unable to find mountpoint\n");
      return -1;
  }

  debug(VFS, "(umount) mountpoint found\n");
  assert(mountpount_path.mnt_);

  // in the case, the current-directory is in the local-root of the umounted
  // filesystem
  if (fs_info->getPwd().mnt_ == mountpount_path.mnt_)
  {
    if (fs_info->getPwd().dentry_ == mountpount_path.dentry_)
    {
      debug(VFS, "(umount) the mount point exchange\n");
      fs_info->setPwd(Path(mountpount_path.mnt_->getMountPoint(), mountpount_path.mnt_->getParent()));
    }
    else
    {
      debug(VFS, "(umount) set PWD NULL\n");
      fs_info->setPwd(Path());
    }
  }

  Superblock *sb = mountpount_path.mnt_->getSuperblock();

  mounts_.remove(mountpount_path.mnt_);
  delete mountpount_path.mnt_;
  delete sb;

  return 0;
}

