#pragma once

#define V3_OFFSET ((superblock_->s_magic_==MINIX_V3) ? 1 : 0)
#define V3_ARRAY(PTR,IDX) ((superblock_->s_magic_==MINIX_V3) ? ((uint32*)(PTR))[(IDX)] : ((uint16*)(PTR))[(IDX)])
#define SET_V3_ARRAY(PTR,IDX,VAL) do { if (superblock_->s_magic_==MINIX_V3) ((uint32*)(PTR))[(IDX)] = VAL; else ((uint16*)(PTR))[(IDX)] = VAL; } while (0)
#define NUM_ZONE_ADDRESSES ((superblock_->s_magic_==MINIX_V3) ? 256 : 512)
#define ZONE_SIZE 1024U
#define BLOCK_SIZE 1024U
#define INODE_BYTES ((superblock_->s_magic_==MINIX_V3) ? 4 : 2)
#define INODE_SIZE ((superblock_->s_magic_==MINIX_V3) ? 64 : 32)
#define INODES_PER_BLOCK ((superblock_->s_magic_==MINIX_V3) ? 16 : 32)
#define DENTRY_SIZE ((superblock_->s_magic_==MINIX_V3) ? 64 : 32)
#define MAX_NAME_LENGTH ((superblock_->s_magic_==MINIX_V3) ? 60 : 30)
#define NUM_ZONES ((superblock_->s_magic_==MINIX_V3) ? 10 : 9)
#define MINIX_V3 0x4d5a

