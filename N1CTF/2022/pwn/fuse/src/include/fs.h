#pragma once
#include <sys/types.h>

#define FSMAGIC 0x636a6673
#define ROOTINO 1
#define BSIZE ((unsigned long)(4096))
#define MAXOPBLOCKS 127
#define NCACHE_BUF (MAXOPBLOCKS * 8)
#define NLOG (MAXOPBLOCKS * 8)

// Disk layout:
// [ boot block (skip) | super block | log | inode blocks |
//                                           free bit map | data blocks]
//
// mkfs will adjust the each section's size and store into the super block.
// as the super block describes the disk layout:
struct superblock {
  uint magic;       // Must be FSMAGIC
  uint size;        // Size of file system image (blocks)
  uint nblocks;     // Number of data blocks
  uint ninodes;     // Number of inodes.
  uint nlog;        // Number of log blocks
  uint logstart;    // Block number of first log block
  uint inodestart;  // Block number of first inode block
  uint bmapstart;   // Block number of first free map block
};
#define SUPERBLOCK_ID 1

#define NDIRECT 43
#define NINDIRECT1 (BSIZE / sizeof(uint))
#define NINDIRECT2 ((BSIZE / sizeof(uint)) * (BSIZE / sizeof(uint)))
#define NINDIRECT3 \
  ((BSIZE / sizeof(uint)) * (BSIZE / sizeof(uint)) * (BSIZE / sizeof(uint)))
#define NINDIRECT (NINDIRECT1 + NINDIRECT2 + NINDIRECT3)
#define NSUBDIRECT 3

#define NBLOCKADDR (NDIRECT + NSUBDIRECT)
#define MAXFILE_BLOCKS (NDIRECT + NINDIRECT)
#define MAXFILE_SIZE ((NDIRECT + NINDIRECT) * BSIZE)

// On-disk inode structure
struct dinode {
  short type;  // File type
  // currently we don't consider the device case
  short major;  // Major device number (T_DEVICE_INODE_MYFUSE only)
  short minor;  // Minor device number (T_DEVICE_INODE_MYFUSE only)
  short nlink;  // Number of links to inode in file system
  size_t size;  // Size of file (bytes)
  struct timespec st_atimespec; /* Nscecs of last access.  */
  struct timespec st_mtimespec; /* Nsecs of last modification.  */
  struct timespec st_ctimespec; /* Nsecs of last status change.  */
  uint perm;                    // permission
  uint addrs[NBLOCKADDR];       // Data block addresses  short type;
};

// Inodes per block.
#define IPB (BSIZE / sizeof(struct dinode))

// Block containing inode i
#define IBLOCK(i) ((i) / IPB + MYFUSE_STATE->sb.inodestart)

// Bitmap bits per block
#define BPB (BSIZE * 8)

// Block of free map containing bit for block b
#define BBLOCK(b) ((b) / BPB + MYFUSE_STATE->sb.bmapstart)

// Directory is a file containing a sequence of dirent structures
struct dirent {
#define DIRSIZE (0x40 - sizeof(uint))
  char name[DIRSIZE];
  uint inum;
};

#define MAX_DIRENT_PERDIR (BSIZE / sizeof(dirent))

// internal used inode type
#define T_UNUSE_INODE_MYFUSE 0
#define T_DIR_INODE_MYFUSE 1
#define T_FILE_INODE_MYFUSE 2
#define T_DEVICE_INODE_MYFUSE 3