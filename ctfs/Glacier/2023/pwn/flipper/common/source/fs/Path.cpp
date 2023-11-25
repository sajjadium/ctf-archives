#include "Path.h"
#include "kprintf.h"
#include "debug.h"
#include "Dentry.h"
#include "VfsMount.h"
#include "Inode.h"
#include "assert.h"
#include "VirtualFileSystem.h"
#include "PathWalker.h"

Path::Path(Dentry* dentry, VfsMount* mnt) :
    dentry_(dentry), mnt_(mnt)
{

}


bool Path::operator==(const Path& other) const
{
    return ((dentry_ == other.dentry_) && (mnt_ == other.mnt_));
}


Path Path::parent(const Path* global_root) const
{
    debug(PATHWALKER, "Walk up to parent dir\n");
    assert(dentry_ && mnt_);

    if(isGlobalRoot(global_root))
    {
        debug(PATHWALKER, "Reached global file system root\n");
        return *this;
    }

    if(isMountRoot())
    {
        debug(PATHWALKER, "File system mount root reached, going up a mount to vfsmount %p, mountpoint %p %s\n", mnt_->getParent(), mnt_->getMountPoint(), mnt_->getMountPoint()->getName());

        return Path(mnt_->getMountPoint()->getParent(), mnt_->getParent());
    }

    return Path(dentry_->getParent(), mnt_);
}

int Path::child(const ustl::string& name, Path& out) const
{ // Warning: out parameter may refer to this object!
    debug(PATHWALKER, "Walk down to child %s\n", name.c_str());
    assert(dentry_ && mnt_);

    VfsMount* child_mnt = mnt_;
    Dentry *child_dentry = dentry_->getInode()->lookup(name.c_str());
    if(!child_dentry)
    {
        debug(PATHWALKER, "Error: No child dentry %s\n", name.c_str());
        out = Path();
        return PW_ENOTFOUND;
    }

#ifndef EXE2MINIXFS
    VfsMount* vfs_mount = vfs.getVfsMount(child_dentry);
    if (vfs_mount != 0)
    {
        debug(PATHWALKER, "Reached mountpoint at %s, going down to mounted file system\n", dentry_->getName());
        assert(child_dentry->getMountedRoot() == vfs_mount->getRoot());

        child_dentry = vfs_mount->getRoot();
        child_mnt = vfs_mount;
    }
#endif

    out = Path(child_dentry, child_mnt);
    return PW_SUCCESS;
}


ustl::string Path::getAbsolutePath(const Path* global_root) const
{
    if(isGlobalRoot(global_root))
    {
        return "/";
    }
    else if(isMountRoot()) // If this is a mount root, we want the name of the mountpoint instead
    {
        return parent().getAbsolutePath() + mnt_->getMountPoint()->getName();
    }
    else if(parent().isGlobalRoot()) // Avoid adding '/' twice
    {
        return parent().getAbsolutePath() + dentry_->getName();
    }
    else
    {
        return parent().getAbsolutePath() + "/" + dentry_->getName();
    }
}

bool Path::isGlobalRoot(const Path* global_root) const
{
    return (global_root && (*this == *global_root)) ||
        (isMountRoot() && mnt_->isRootMount());
}

bool Path::isMountRoot() const
{
    return dentry_->getParent() == dentry_;
}
