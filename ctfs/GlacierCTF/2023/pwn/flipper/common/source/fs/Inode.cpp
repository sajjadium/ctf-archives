#include "Inode.h"
#include "Superblock.h"
#include "FileSystemType.h"
#include "File.h"

Inode::Inode(Superblock *superblock, uint32 inode_type) :
    i_dentrys_(),
    i_files_(),
    i_nlink_(0),
    i_refcount_(0),
    superblock_(superblock),
    i_size_(0),
    i_type_(inode_type),
    i_state_(I_UNUSED),
    i_mode_((A_READABLE ^ A_WRITABLE) ^ A_EXECABLE)
{
}

Inode::~Inode()
{
    if(numRefs() != 0)
    {
        debug(INODE, "~Inode %s %p refcount: %u\n", getSuperblock()->getFSType()->getFSName(), this, numRefs());
    }
    assert(numRefs() == 0);
}

uint32 Inode::incRefCount()
{
    auto count = ++i_refcount_;
    debug(INODE, "Increasing %s inode %p ref count to: %u\n", getSuperblock()->getFSType()->getFSName(), this, count);
    return count;
}

uint32 Inode::decRefCount()
{
    auto count = --i_refcount_;
    debug(INODE, "Decreasing %s inode %p ref count to: %u\n", getSuperblock()->getFSType()->getFSName(), this, count);
    return count;
}

uint32 Inode::incLinkCount()
{
    auto count = ++i_nlink_;
    debug(INODE, "Increasing %s inode %p link count to: %u\n", getSuperblock()->getFSType()->getFSName(), this, count);
    return count;
}

uint32 Inode::decLinkCount()
{
    auto count = --i_nlink_;
    debug(INODE, "Decreasing %s inode %p link count to: %u\n", getSuperblock()->getFSType()->getFSName(), this, count);
    return count;
}

uint32 Inode::numRefs()
{
    return i_refcount_;
}

uint32 Inode::numLinks()
{
    return i_nlink_;
}


bool Inode::hasDentry(Dentry* dentry)
{
    return ustl::find(i_dentrys_.begin(), i_dentrys_.end(), dentry) != i_dentrys_.end();
}

void Inode::addDentry(Dentry* dentry)
{
    assert(dentry);
    assert(!hasDentry(dentry));

    debug(INODE, "%s inode %p addDentry %s\n",
          getSuperblock()->getFSType()->getFSName(), this, dentry->getName());

    incRefCount();

    i_dentrys_.push_back(dentry);
    dentry->setInode(this);
}

void Inode::removeDentry(Dentry* dentry)
{
    assert(dentry);
    assert(dentry->getInode() == this);
    assert(hasDentry(dentry));

    debug(INODE, "%s inode %p removeDentry %s\n",
          getSuperblock()->getFSType()->getFSName(), this, dentry->getName());

    i_dentrys_.remove(dentry);
    assert(!hasDentry(dentry));

    dentry->releaseInode();
    decRefCount();
}



// ########################
// Default inode operations
// ########################

int32 Inode::mkfile(Dentry* dentry)
{
    assert(dentry);
    assert(dentry->getInode() == this);
    assert(hasDentry(dentry));
    assert(getType() == I_FILE);

    debug(INODE, "%s inode %p mkfile %s\n",
          getSuperblock()->getFSType()->getFSName(), this, dentry->getName());

    incLinkCount();
    return 0;
}

int32 Inode::mkdir(Dentry* dentry)
{
    assert(dentry);
    assert(dentry->getInode() == this);
    assert(hasDentry(dentry));
    assert(getType() == I_DIR);

    debug(INODE, "%s inode %p mkdir %s\n",
          getSuperblock()->getFSType()->getFSName(), this, dentry->getName());

    incLinkCount();
    return 0;
}

int32 Inode::mknod(Dentry* dentry)
{
    assert(dentry);
    assert(dentry->getInode() == this);
    assert(hasDentry(dentry));
    assert((getType() != I_DIR) && (getType() != I_FILE));

    debug(INODE, "%s inode %p mkdir %s\n",
          getSuperblock()->getFSType()->getFSName(), this, dentry->getName());

    incLinkCount();
    return 0;
}

int32 Inode::link(Dentry* dentry)
{
    assert(dentry);
    assert(dentry->getInode() == this);
    assert(hasDentry(dentry));

    if(getType() == I_DIR)
    {
        debug(INODE, "Hard links are not supported for directories\n");
        return -1;
    }

    debug(INODE, "%s indode %p link %s\n",
          getSuperblock()->getFSType()->getFSName(), this, dentry->getName());

    incLinkCount();
    return 0;
}

int32 Inode::unlink(Dentry* dentry)
{
    assert(dentry);
    assert(dentry->getInode() == this);
    assert(hasDentry(dentry));

    debug(INODE, "%s inode %p unlink %s\n",
          getSuperblock()->getFSType()->getFSName(), this, dentry->getName());

    if(!dentry->emptyChild())
    {
        debug(INODE, "Error: %s inode %p has children, cannot unlink %s\n",
              getSuperblock()->getFSType()->getFSName(), this, dentry->getName());
        return -1;
    }

    decLinkCount();
    return 0;
}

int32 Inode::rmdir(Dentry* dentry)
{
    assert(dentry);
    assert(dentry->getInode() == this);
    assert(hasDentry(dentry));
    assert(getType() == I_DIR);

    debug(INODE, "%s inode %p rmdir %s\n",
          getSuperblock()->getFSType()->getFSName(), this, dentry->getName());

    if(!dentry->emptyChild())
    {
        debug(INODE, "Error: %s inode %p has children, cannot unlink %s\n",
              getSuperblock()->getFSType()->getFSName(), this, dentry->getName());
        return -1;
    }

    decLinkCount();
    return 0;
}

Dentry* Inode::lookup(const char* name)
{
    if (name == 0)
    {
        // ERROR_DNE
        return 0;
    }

    debug(INODE, "%s inode %p lookup %s\n", getSuperblock()->getFSType()->getFSName(), this, name);

    if (i_type_ != I_DIR)
    {
        return 0;
    }

    assert(i_dentrys_.size() >= 1);
    return i_dentrys_.front()->checkName(name);
}


int32 Inode::release(File* file)
{
    debug(INODE, "%s inode %p release file\n", getSuperblock()->getFSType()->getFSName(), this);
    i_files_.remove(file);
    getSuperblock()->fileReleased(file);
    delete file;
    return 0;
}
