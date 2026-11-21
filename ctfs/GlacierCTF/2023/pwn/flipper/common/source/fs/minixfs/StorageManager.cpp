#include "StorageManager.h"

StorageManager::StorageManager(uint16 num_inodes, uint16 num_zones) :
    inode_bitmap_(num_inodes), zone_bitmap_(num_zones)
{
}

StorageManager::~StorageManager()
{
}

