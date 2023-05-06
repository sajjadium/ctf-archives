#pragma once
#include <gtest/gtest.h>
#include "mkfs.myfuse-util.h"

#define MAX_SECTOR_BLOCK_NO 400000
static_assert(MAX_SECTOR_BLOCK_NO % sector_per_block == 0,
              "test disk unaligned!");
#define MAX_BLOCK_NO MAX_SECTOR_BLOCK_NO / sector_per_block
extern int nmeta_blocks;

class TestEnvironment : public ::testing::Environment {
 public:
  void SetUp() override {
    srand(time(nullptr));

#ifndef DISK_IMG_PATH
#define DISK_IMG_PATH "./disk.img"
#endif
    block_device_init(DISK_IMG_PATH);

    init_super_block(MAX_BLOCK_NO);

    nmeta_blocks = MYFUSE_STATE->sb.size - MYFUSE_STATE->sb.nblocks;
    std::array<u_char, BSIZE> zeros;
    zeros.fill(0);
    for (int i = 0; i < nmeta_blocks; i++) {
      write_block_raw(i, zeros.data());
    }
    memmove(zeros.data(), &MYFUSE_STATE->sb, sizeof(MYFUSE_STATE->sb));
    write_block_raw(1, zeros.data());

    bcache_init();
    log_init(&MYFUSE_STATE->sb);

    inode_init(&MYFUSE_STATE->sb);
    init_meta_blocks_bmap();
    block_allocator_refresh(&MYFUSE_STATE->sb);

    add_rootinode();

    file_init();
  }
};

const int content_sum = 1000;
const int MAX_WORKER  = 10;

// map blockno to it's expected content
extern std::map<int, const u_char*> contents;
// this array contains {content_sum} uniq random nums in range [0,
// MAX_BLOCK_NO)
extern std::array<int, content_sum> content_blockno;
void generate_block_test_data();

void start_worker(void* (*pthread_worker)(void*), uint MAXWORKER = MAX_WORKER,
                  uint64_t end = content_sum);

// indicate the range the worker need to workon
// don't free it by the callee
struct start_to_end {
  uint start;
  uint end;
};