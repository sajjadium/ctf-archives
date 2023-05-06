#include <cmath>
#include "mkfs.myfuse-util.h"
#include <cassert>

void init_super_block(uint disk_size_in_sector_block) {
  auto sb = &MYFUSE_STATE->sb;

  const uint disk_size     = disk_size_in_sector_block;
  const uint nlog          = NLOG;
  const uint nbitmap       = (ROUNDUP(disk_size, BPB)) / BPB;
  const uint ninode_blocks = ceil(disk_size / 50) + 1;
  const uint ninodes       = ninode_blocks * IPB;
  const uint nmeta_blocks  = 2 + nlog + ninode_blocks + nbitmap;
  const uint nblocks       = disk_size - nmeta_blocks;
  sb->magic                = FSMAGIC;
  sb->ninodes              = ninodes;
  sb->size                 = disk_size;
  sb->nblocks              = nblocks;
  sb->nlog                 = nlog;
  sb->logstart             = 2;
  sb->inodestart           = 2 + nlog;
  sb->bmapstart            = 2 + nlog + ninode_blocks;

  const double ONEK = 1024.0;
  myfuse_log("this disk can have about %.2lf GiB storage",
             ((nblocks * BSIZE) / ONEK / ONEK / ONEK) * 0.96);
  printf(
      "nmeta %d (boot, super, log blocks %u, inode blocks %u, bitmap blocks "
      "%u)\n"
      "blocks %d total %d\n",
      nmeta_blocks, nlog, ninode_blocks, nbitmap, nblocks, disk_size);
  printf("%ld bytes per-block\n", BSIZE);
}

struct myfuse_state* get_myfuse_state() {
  static struct myfuse_state state;
  return &state;
}

void add_rootinode() {
  begin_op();
  auto ip = ialloc(T_DIR_INODE_MYFUSE);

  assert(ip->inum == ROOTINO);
  ilock(ip);
  ip->nlink = 1;
  ip->type  = T_DIR_INODE_MYFUSE;
  get_current_timespec(&ip->st_atimespec);
  ip->st_ctimespec = ip->st_mtimespec = ip->st_atimespec;
  iupdate(ip);
  // fuse need no . or ..
  //  dirlink(ip, ".", ip->inum);
  //  dirlink(ip, "..", ip->inum);
  iunlockput(ip);
  end_op();
}
