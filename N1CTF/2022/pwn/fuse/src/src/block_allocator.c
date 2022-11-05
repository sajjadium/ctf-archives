#include "block_allocator.h"
#include "log.h"
#include <assert.h>

struct bmap_cache bmap_cache;

void block_allocator_refresh(struct superblock* sb) {
  // init the bmap cache
  uint ncache_blocks   = ROUNDUP(sb->size, BPB) / BPB;
  bmap_cache.cache_buf = realloc(bmap_cache.cache_buf, ncache_blocks * BSIZE);
  bmap_cache.first_unalloced =
      realloc(bmap_cache.first_unalloced, ncache_blocks * sizeof(uint));
  bmap_cache.n_alloced =
      realloc(bmap_cache.n_alloced, ncache_blocks * sizeof(uint));
  bmap_cache.n_cache = ncache_blocks;
  pthread_mutex_init(&bmap_cache.lock, NULL);
  begin_op();
  uint blockno    = 0;
  uint first_free = 0;
  for (uint i = 0; i < ncache_blocks; i++) {
    struct bcache_buf* bp = logged_read(i + sb->bmapstart);

    memmove(bmap_cache.cache_buf + i * BSIZE, bp->data, BSIZE);
    logged_relse(bp);

    // get the first unalloced block and calc the sum of alloced blocks
    int first_unalloced     = -1;
    bmap_cache.n_alloced[i] = 0;
    for (uint j = 0; j < BPB; j++) {
      if (bmap_block_statue_get(blockno)) {
        bmap_cache.n_alloced[i]++;
      } else {
        if (first_unalloced == -1) {
          first_unalloced = blockno % BPB;
        }
      }
      blockno++;
    }
    bmap_cache.first_unalloced[i] = first_unalloced;
    if (first_unalloced != -1 && first_free != 0) {
      first_free = i;
    }
  }
  end_op();

  if (bmap_cache.first_free_cache < 0) {
    myfuse_nonfatal(
        "no more free space in the file system\n"
        "any write operation will cause a crash");
  }
}

int bmap_block_statue_get(uint blockno) {
  uint byte = blockno / 8;
  uint bit  = blockno % 8;
  return (bmap_cache.cache_buf[byte] >> bit) & 1;
}

// set bmap's blockno's bit to i (0 / 1)
void bmap_block_statue_set(uint blockno, int i) {
#ifdef DEBUG
  assert((blockno / BPB) < bmap_cache.n_cache);
#endif
  uint byte      = blockno / 8;
  uint bit       = blockno % 8;
  char bits_flag = bmap_cache.cache_buf[byte];
  i              = i & 1;  // only use the last bit;
  if (i) {
    // ones it
    bits_flag |= ((u_char)1) << bit;
  } else {
    // zeros it
    bits_flag &= ~(((u_char)1) << bit);
  }
  bmap_cache.cache_buf[byte] = bits_flag;
  // write back to disk
  uint bmapno             = blockno / BPB + MYFUSE_STATE->sb.bmapstart;
  uint bmap_byte_off      = (blockno % BPB) / 8;
  struct bcache_buf* bp   = logged_read(bmapno);
  bp->data[bmap_byte_off] = bits_flag;
  logged_write(bp);
  logged_relse(bp);
}

void init_meta_blocks_bmap() {
  uint nmeta_bloks = MYFUSE_STATE->sb.size - MYFUSE_STATE->sb.nblocks;
  for (int i = 0; i < nmeta_bloks; i++) {
    begin_op();
    bmap_block_statue_set(i, 1);
    end_op();
  }

  for (int i = MYFUSE_STATE->sb.size; i < ROUNDUP(MYFUSE_STATE->sb.size, BPB);
       i++) {
    begin_op();
    bmap_block_statue_set(i, 1);
    end_op();
  }
}

void logged_zero_a_block(uint bno) {
  struct bcache_buf* bp = logged_read(bno);
  memset(bp->data, 0, BSIZE);
  logged_write(bp);
  logged_relse(bp);
}

static inline uint bmap2blockno(uint bmapno, uint bmap_cache_index) {
  return bmapno + bmap_cache_index * BPB;
}

uint block_alloc() {
  pthread_mutex_lock(&bmap_cache.lock);
  uint free_cache_index = bmap_cache.first_free_cache;
  if (free_cache_index < 0) {
    err_exit("no more free space in disk!");
  }
  uint first_free_block = bmap_cache.first_unalloced[free_cache_index];
  DEBUG_TEST(assert(first_free_block >= 0););
  // fisrt, get the block
  uint victim_blockno = bmap2blockno(first_free_block, free_cache_index);

  // second, set the block to alloced
  DEBUG_TEST(assert(bmap_block_statue_get(victim_blockno) == 0););
  bmap_block_statue_set(victim_blockno, 1);

  // third, update the cache
  bmap_cache.n_alloced[free_cache_index]++;
  if (bmap_cache.n_alloced[free_cache_index] == BPB) {
    // this cache is full, find the next one
    int find                                     = 0;
    bmap_cache.first_unalloced[free_cache_index] = -1;
    for (uint i = 0; i < bmap_cache.n_cache; i++) {
      if (bmap_cache.first_unalloced[i] != -1) {
        find                        = 1;
        bmap_cache.first_free_cache = i;
        break;
      }
    }

    if (find == 0) {
      bmap_cache.first_free_cache = -1;
      err_exit("no more free space in disk!");
    }
  } else {
    // find the next free block
    for (uint i = first_free_block + 1; i < BPB; i++) {
      if (bmap_block_statue_get(bmap2blockno(i, free_cache_index)) == 0) {
        bmap_cache.first_unalloced[free_cache_index] = i;
        break;
      }
    }
  }

  pthread_mutex_unlock(&bmap_cache.lock);

  // fourth, zero the block and return
  logged_zero_a_block(victim_blockno);
  return victim_blockno;
}

void block_free(uint blockno) {
  pthread_mutex_lock(&bmap_cache.lock);
  uint cache_index = blockno / BPB;
  uint bmapno      = blockno % BPB;

  // first, set the block to free
  DEBUG_TEST(assert(bmap_block_statue_get(blockno) == 1); /* double free */);
  bmap_block_statue_set(blockno, 0);

  // second, set the cache
  bmap_cache.n_alloced[cache_index]--;
  bmap_cache.first_unalloced[cache_index] =
      bmap_cache.first_unalloced[cache_index] > bmapno
          ? bmapno
          : bmap_cache.first_unalloced[cache_index];
  bmap_cache.first_free_cache = cache_index;

  pthread_mutex_unlock(&bmap_cache.lock);
  return;
}