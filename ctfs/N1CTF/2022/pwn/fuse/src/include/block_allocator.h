// this is dedicated to inode layer
#pragma once
#include "param.h"

// bitmap's in memory representation
struct bmap_cache {
  char* cache_buf;
  int* first_unalloced;  // -1 indicate the block is full
  uint* n_alloced;
  uint n_cache;
  uint first_free_cache;  // -1 indicate no free space in disk
  pthread_mutex_t lock;
};

extern struct bmap_cache bmap_cache;

void block_allocator_refresh(struct superblock* sb);

void bmap_block_statue_set(uint blockno, int i);
int bmap_block_statue_get(uint blockno);

// this is for the test
void init_meta_blocks_bmap();

uint block_alloc();
void block_free(uint blockno);

void logged_zero_a_block(uint blockno);
