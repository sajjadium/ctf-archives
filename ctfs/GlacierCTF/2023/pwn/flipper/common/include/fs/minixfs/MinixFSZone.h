#pragma once

#include "types.h"

class MinixFSSuperblock;

class MinixFSZone
{
  public:

    /**
     * constructor
     * @param superblock the superblock
     * @param zones the zone array from the file system
     */
    MinixFSZone(MinixFSSuperblock *superblock, uint32 *zones);
    ~MinixFSZone();
    uint32 getZone(uint32 index);
    void setZone(uint32 index, uint32 zone);
    void addZone(uint32 zone);
    uint32 getNumZones()
    {
      return num_zones_;
    }
    void flush(uint32 inode_num);
    void freeZones();

  private:

    MinixFSSuperblock *superblock_;
    uint32 direct_zones_[10];
    uint32 *indirect_zones_;
    uint32 *double_indirect_linking_zone_;
    uint32 **double_indirect_zones_;

    uint32 num_zones_;

};

