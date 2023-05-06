#include <cstdio>
#include <cmath>
#include <unistd.h>
#include <cstdlib>
#include <cstring>
#include <fcntl.h>
#include <cassert>
#include <sys/stat.h>
#include <algorithm>
#include <string>
#include <iostream>
#include <malloc.h>

// this give us some utilities
#include "mkfs.myfuse-util.h"

// Disk layout
// [ boot block (skip) | super block | log | inode blocks |
//                                           free bit map | data blocks]

int main(int argc, char* argv[]) {
  std::string user_decide;
  std::string disk_name;

  if (argc != 2) {
    err_exit(
        "Usage: %s /dev/<disk name>\n"
        "\tNote: the disk will be treated as sector size of 512\n",
        argv[0]);
  }

  disk_name = argv[1];

  static_assert(BSIZE % sizeof(struct dinode) == 0);
  static_assert(BSIZE % sizeof(struct dirent) == 0);

  myfuse_log(
      "This program will format the disk %s\n"
      "Continue? yes/no >>",
      disk_name.c_str());
  std::cin >> user_decide;
  std::transform(user_decide.begin(), user_decide.end(), user_decide.begin(),
                 [](unsigned char c) { return std::tolower(c); });
  if (user_decide.substr(0, 3) != "yes") {
    err_exit("canceled");
  }

  std::string blockdev_command{"blockdev --getsz "};
  blockdev_command += disk_name;

  auto blockdev_reslut = popen(blockdev_command.c_str(), "r");
  uint sector_size;
  fscanf(blockdev_reslut, "%u", &sector_size);
  myfuse_log("sector size: %d", sector_size);
  pclose(blockdev_reslut);

  uint block_size = sector_size / sector_per_block;

  if (block_size <= 100) {
    err_exit("block size too small");
  }
  block_device_init(disk_name.c_str());
  init_super_block(block_size);
  std::array<u_char, BSIZE> zeros;
  uint nmeta_blocks = MYFUSE_STATE->sb.size - MYFUSE_STATE->sb.nblocks;
  zeros.fill(0);
  for (uint i = 0; i < nmeta_blocks; i++) {
    write_block_raw(i, zeros.data());
  }
  memmove(zeros.data(), &MYFUSE_STATE->sb, sizeof(MYFUSE_STATE->sb));
  write_block_raw(1, zeros.data());

  bcache_init();
  log_init(&MYFUSE_STATE->sb);

  inode_init(&MYFUSE_STATE->sb);

  for (uint i = 0; i < ROUNDUP(MYFUSE_STATE->sb.size, BPB) / BPB; i++) {
    begin_op();
    logged_zero_a_block(MYFUSE_STATE->sb.bmapstart + i);
    end_op();
  }
  block_allocator_refresh(&MYFUSE_STATE->sb);
  init_meta_blocks_bmap();
  block_allocator_refresh(&MYFUSE_STATE->sb);

  // write sb to disk
  begin_op();
  auto sbi = logged_read(1);
  memmove(sbi->data, &MYFUSE_STATE->sb, sizeof(struct superblock));
  logged_write(sbi);
  logged_relse(sbi);
  end_op();

  add_rootinode();

  return 0;
}
