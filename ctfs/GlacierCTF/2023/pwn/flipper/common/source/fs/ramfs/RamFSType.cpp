#include "fs/ramfs/RamFSType.h"
#include "fs/ramfs/RamFSSuperblock.h"


RamFSType::RamFSType() : FileSystemType("ramfs")
{
}


RamFSType::~RamFSType()
{}


Superblock *RamFSType::readSuper(Superblock *superblock, void*) const
{
  return superblock;
}


Superblock *RamFSType::createSuper (uint32 s_dev)
{
  Superblock *super = new RamFSSuperblock(this, s_dev);
  return super;
}
