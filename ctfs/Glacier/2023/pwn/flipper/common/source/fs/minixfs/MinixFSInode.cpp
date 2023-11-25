#include "MinixFSInode.h"
#ifndef EXE2MINIXFS
#include "kstring.h"
#endif
#include <assert.h>
#include "MinixFSSuperblock.h"
#include "MinixFSFile.h"
#include "Dentry.h"

MinixFSInode::MinixFSInode(Superblock *super_block, uint32 inode_type) :
    Inode(super_block, inode_type),
    i_zones_(0),
    i_num_(0),
    children_loaded_(false)
{
  debug(M_INODE, "Simple Constructor\n");
}

MinixFSInode::MinixFSInode(Superblock *super_block, uint16 i_mode, uint32 i_size, uint16 i_nlinks, uint32* i_zones,
                           uint32 i_num) :
    Inode(super_block, 0), i_zones_(new MinixFSZone((MinixFSSuperblock*) super_block, i_zones)), i_num_(i_num),
    children_loaded_(false)
{
  i_size_ = i_size;
  i_nlink_ = i_nlinks;
  i_state_ = I_UNUSED;
  if (i_mode & 0x8000)
  {
    i_type_ = I_FILE;
  }
  else if (i_mode & 0x4000)
  {
    i_type_ = I_DIR;
  }
  else
  {
    debug(M_INODE, "i_mode = %x\n", i_mode);
    assert(false);
  }
  // (hard/sym link/...) not handled!

  debug(M_INODE, "Constructor: size: %d\tnlink: %d\tnum zones: %d\tmode: %x\n", i_size_, numLinks(),
        i_zones_->getNumZones(), i_mode);
}

MinixFSInode::~MinixFSInode()
{
  debug(M_INODE, "Destructor\n");
  delete i_zones_;
}

int32 MinixFSInode::readData(uint32 offset, uint32 size, char *buffer)
{
  assert(buffer);
  debug(M_INODE, "readData: offset: %d, size; %d,i_size_: %d\n", offset, size, i_size_);
  if ((size + offset) > i_size_)
  {
    if (i_size_ <= offset)
      return 0;
    else
      size = i_size_ - offset;
  }
  uint32 start_zone = offset / ZONE_SIZE;
  uint32 zone_offset = offset % ZONE_SIZE;
  uint32 num_zones = (zone_offset + size) / ZONE_SIZE + 1;
  char rbuffer[ZONE_SIZE];

  uint32 index = 0;
  debug(M_INODE, "readData: zone: %d, zone_offset %d, num_zones: %d\n", start_zone, zone_offset, num_zones);
  for (uint32 zone = start_zone; zone < start_zone + num_zones; zone++)
  {
    memset(rbuffer, 0, sizeof(rbuffer));
    ((MinixFSSuperblock *) superblock_)->readZone(i_zones_->getZone(zone), rbuffer);
    uint32 count = size - index;
    uint32 zone_diff = ZONE_SIZE - zone_offset;
    count = count < zone_diff ? count : zone_diff;
    memcpy(buffer + index, rbuffer + zone_offset, count);
    index += count;
    zone_offset = 0;
  }
  return size;
}

int32 MinixFSInode::writeData(uint32 offset, uint32 size, const char *buffer)
{
  debug(M_INODE, "MinixFSInode writeData> offset: %d, size: %d, i_size_: %d\n", offset, size, i_size_);
  uint32 zone = offset / ZONE_SIZE;
  uint32 num_zones = (offset % ZONE_SIZE + size) / ZONE_SIZE + 1;
  uint32 last_used_zone = i_size_ / ZONE_SIZE;
  uint32 last_zone = last_used_zone;
  if ((size + offset) > i_size_)
  {
    uint32 num_new_zones = (size + offset - i_size_) / ZONE_SIZE + 1;
    for (uint32 new_zones = 0; new_zones < num_new_zones; new_zones++, last_zone++)
    {
      MinixFSSuperblock* sb = (MinixFSSuperblock*) superblock_;
      debug(M_INODE, "writeData: allocating new Zone\n");
      uint16 new_zone = sb->allocateZone();
      i_zones_->setZone(i_zones_->getNumZones(), new_zone);
    }
  }
  if (offset > i_size_)
  {
    debug(M_INODE, "writeData: have to clean memory\n");
    uint32 zone_size_offset = i_size_ % ZONE_SIZE;
    char fill_buffer[ZONE_SIZE];
    memset(fill_buffer, 0, sizeof(fill_buffer));
    if (zone_size_offset)
    {
      readData(i_size_ - zone_size_offset, zone_size_offset, fill_buffer);
      ((MinixFSSuperblock *) superblock_)->writeZone(last_used_zone, fill_buffer);
    }
    ++last_used_zone;
    for (; last_used_zone <= offset / ZONE_SIZE; last_used_zone++)
    {
      memset(fill_buffer, 0, sizeof(fill_buffer));
      ((MinixFSSuperblock *) superblock_)->writeZone(last_used_zone, fill_buffer);
    }
    --last_used_zone;
    i_size_ = offset;
  }
  uint32 zone_offset = offset % ZONE_SIZE;
  char* wbuffer_array = new char[num_zones * ZONE_SIZE];
  char* wbuffer = wbuffer_array;
  memset((void*) wbuffer, 0, num_zones * ZONE_SIZE);
  debug(M_INODE, "writeData: reading data at the beginning of zone: offset-zone_offset: %d,zone_offset: %d\n",
        offset - zone_offset, zone_offset);
  readData(offset - zone_offset, num_zones * ZONE_SIZE, wbuffer);
  for (uint32 index = 0, pos = zone_offset; index < size; pos++, index++)
  {
    wbuffer[pos] = buffer[index];
  }
  for (uint32 zone_index = 0; zone_index < num_zones; zone_index++)
  {
    debug(M_INODE, "writeData: writing zone_index: %d, i_zones_->getZone(zone) : %d\n", zone_index,
          i_zones_->getZone(zone));
    ((MinixFSSuperblock *) superblock_)->writeZone(i_zones_->getZone(zone_index + zone), wbuffer);
    wbuffer += ZONE_SIZE;
  }
  if (i_size_ < offset + size)
  {
    i_size_ = offset + size;
  }
  delete[] wbuffer_array;
  return size;
}

int32 MinixFSInode::mknod(Dentry *dentry)
{
  Inode::mknod(dentry);
  debug(M_INODE, "mknod: dentry: %p, i_type_: %x\n", dentry, i_type_);

  ((MinixFSInode *) dentry->getParent()->getInode())->writeDentry(0, i_num_, dentry->getName());
  return 0;
}

int32 MinixFSInode::mkfile(Dentry *dentry)
{
  Inode::mkfile(dentry);
  debug(M_INODE, "mkfile: dentry: %p (%s)\n", dentry, dentry->getName());

  ((MinixFSInode *) dentry->getParent()->getInode())->writeDentry(0, i_num_, dentry->getName());
  return 0;
}

int32 MinixFSInode::mkdir(Dentry *dentry)
{
  Inode::mkdir(dentry);
  debug(M_INODE, "mkdir: dentry: %p (%s)\n", dentry, dentry->getName());

  MinixFSInode* parent_inode = ((MinixFSInode *) dentry->getParent()->getInode());
  assert(parent_inode->getType() == I_DIR);

  parent_inode->writeDentry(0, i_num_, dentry->getName());
  // link count already increased once in Inode::mkdir(dentry);

  writeDentry(0, i_num_, ".");
  incLinkCount();

  writeDentry(0, parent_inode->i_num_, "..");
  parent_inode->incLinkCount();

  return 0;
}

int32 MinixFSInode::findDentry(uint32 i_num)
{
  debug(M_INODE, "findDentry: i_num: %d\n", i_num);
  char dbuffer[ZONE_SIZE];
  for (uint32 zone = 0; zone < i_zones_->getNumZones(); zone++)
  {
    ((MinixFSSuperblock *) superblock_)->readZone(i_zones_->getZone(zone), dbuffer);
    for (uint32 curr_dentry = 0; curr_dentry < BLOCK_SIZE; curr_dentry += INODE_SIZE)
    {
      uint16 inode_index = *(uint16*) (dbuffer + curr_dentry);
      if (inode_index == i_num)
      {
        debug(M_INODE, "findDentry: found pos: %d\n", (zone * ZONE_SIZE + curr_dentry));
        return (zone * ZONE_SIZE + curr_dentry);
      }
    }
  }
  debug(M_INODE, "findDentry: i_num: %d not found\n", i_num);
  return -1;
}

void MinixFSInode::writeDentry(uint32 dest_i_num, uint32 src_i_num, const char* name)
{
  debug(M_INODE, "writeDentry: dest_i_num : %d, src_i_num : %d, name : %s\n", dest_i_num, src_i_num, name);
  assert(name);
  int32 dentry_pos = findDentry(dest_i_num);
  if (dentry_pos < 0 && dest_i_num == 0)
  {
    i_zones_->addZone(((MinixFSSuperblock *) superblock_)->allocateZone());
    dentry_pos = (i_zones_->getNumZones() - 1) * ZONE_SIZE;
  }
  char dbuffer[ZONE_SIZE];
  uint32 zone = i_zones_->getZone(dentry_pos / ZONE_SIZE);
  ((MinixFSSuperblock *) superblock_)->readZone(zone, dbuffer);
  *(uint16*) (dbuffer + (dentry_pos % ZONE_SIZE)) = src_i_num;
  strncpy(dbuffer + dentry_pos % ZONE_SIZE + INODE_BYTES, name, MAX_NAME_LENGTH);
  ((MinixFSSuperblock *) superblock_)->writeZone(zone, dbuffer);

  if (dest_i_num == 0 && i_size_ < (uint32) dentry_pos + INODE_SIZE)
    i_size_ += INODE_SIZE;

}

File* MinixFSInode::open(Dentry* dentry, uint32 flag)
{
  debug(M_INODE, "Open file, flag: %x\n", flag);
  assert(ustl::find(i_dentrys_.begin(), i_dentrys_.end(), dentry) != i_dentrys_.end());
  File* file = (File*) (new MinixFSFile(this, dentry, flag));
  i_files_.push_back(file);
  getSuperblock()->fileOpened(file);
  return file;
}


int32 MinixFSInode::link(Dentry* dentry)
{
    int32 link_status = Inode::link(dentry);
    if(link_status)
    {
        return link_status;
    }

    ((MinixFSInode *) dentry->getParent()->getInode())->writeDentry(0, i_num_, dentry->getName());

    return 0;
}

int32 MinixFSInode::unlink(Dentry* dentry)
{
    int32 unlink_status = Inode::unlink(dentry);
    if(unlink_status)
    {
        return unlink_status;
    }

    ((MinixFSInode *) dentry->getParent()->getInode())->writeDentry(i_num_, 0, "");

    return 0;
}

int32 MinixFSInode::rmdir(Dentry* dentry)
{
  assert(dentry && (dentry->getInode() == this));
  assert(dentry->getParent() && (dentry->getParent()->getInode()));
  assert(getType() == I_DIR);

  debug(M_INODE, "rmdir %s for inode %p\n", dentry->getName(), this);

  MinixFSInode* parent_inode = static_cast<MinixFSInode*>(dentry->getParent()->getInode());

  //the "." and ".." dentries will be deleted in some inode-dtor
  //("." in this inodes-dtor, ".." in the parent-dentry-inodes-dtor)
  for (Dentry* child : dentry->d_child_)
  {
    if (strcmp(child->getName(), ".") != 0 && strcmp(child->getName(), "..") != 0)
    {
      //if directory contains other entries than "." or ".."
      //-> directory not empty
      debug(M_INODE, "Error: Cannot remove non-empty directory\n");
      return -1;
    }
  }

  writeDentry(i_num_, 0, ""); //this was the "."-entry
  decLinkCount();

  writeDentry(parent_inode->i_num_, 0, ""); //this was ".."
  parent_inode->decLinkCount();

  parent_inode->writeDentry(i_num_, 0, "");
  decLinkCount();

  assert(i_nlink_ == 0);

  return 0;
}

Dentry* MinixFSInode::lookup(const char* name)
{
  if(i_type_ != I_DIR)
  {
    return nullptr;
  }

  assert(i_dentrys_.size() >= 1);

  debug(M_INODE, "lookup: name: %s this->i_dentry_->getName(): %s \n", name, i_dentrys_.front()->getName());
  if (name == 0)
  {
    // ERROR_DNE
    return 0;
  }

  Dentry* dentry_update = 0;

  dentry_update = i_dentrys_.front()->checkName(name);
  if (dentry_update == 0)
  {
    // ERROR_NNE
    return (Dentry*) 0;
  }
  else
  {
    debug(M_INODE, "lookup: dentry_update->getName(): %s\n", dentry_update->getName());
    if (((MinixFSInode *) dentry_update->getInode())->i_type_ == I_DIR)
    {
      ((MinixFSInode *) dentry_update->getInode())->loadChildren();
    }
    return dentry_update;
  }
}

void MinixFSInode::loadChildren()
{
  if (children_loaded_)
  {
    debug(M_INODE, "loadChildren: Children allready loaded\n");
    return;
  }
  char dbuffer[ZONE_SIZE];
  for (uint32 zone = 0; zone < i_zones_->getNumZones(); zone++)
  {
    ((MinixFSSuperblock *) superblock_)->readZone(i_zones_->getZone(zone), dbuffer);
    for (uint32 curr_dentry = 0; curr_dentry < BLOCK_SIZE; curr_dentry += INODE_SIZE)
    {
      uint16 inode_index = *(uint16*) (dbuffer + curr_dentry);
      if (inode_index)
      {
        debug(M_INODE, "loadChildren: loading child %d\n", inode_index);
        bool is_already_loaded = false;

        MinixFSInode* inode = ((MinixFSSuperblock *) superblock_)->getInode(inode_index, is_already_loaded);

        if (!inode)
        {
          kprintfd("MinixFSInode::loadChildren: inode nr. %d not set in bitmap, but occurs in directory-entry; "
                   "maybe filesystem was not properly unmounted last time\n",
                   inode_index);
          char ch = 0;
          writeDentry(inode_index, 0, &ch);
          continue;
        }

        char name[MAX_NAME_LENGTH + 1];
        strncpy(name, dbuffer + curr_dentry + INODE_BYTES, MAX_NAME_LENGTH);

        name[MAX_NAME_LENGTH] = 0;

        debug(M_INODE, "loadChildren: dentry name: %s\n", name);
        assert(i_dentrys_.size() >= 1);
        Dentry *new_dentry = new Dentry(inode, i_dentrys_.front(), name);
        inode->i_dentrys_.push_back(new_dentry);

        if (!is_already_loaded)
        {
          ((MinixFSSuperblock *) superblock_)->all_inodes_add_inode(inode);
        }
      }
    }
  }
  children_loaded_ = true;
}

int32 MinixFSInode::flush()
{
  superblock_->writeInode(this);
  debug(M_INODE, "flush: flushed\n");
  return 0;
}
