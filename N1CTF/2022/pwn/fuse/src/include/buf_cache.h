#pragma once
#include "param.h"
#include "pthread.h"

struct bcache_buf {
  int valid;  // has data read from disk?
  uint blockno;
  pthread_mutex_t lock;
  uint refcnt;
  struct bcache_buf* prev;
  struct bcache_buf* next;
  uint64_t timestamp;
  u_char data[BSIZE];
};

// buffed read and write
// Return a locked buf with the contents of the indicated block
struct bcache_buf* bread(uint blockno);

// Write back block to disk
// @return nbytes wrote [only for test]
int bwrite(struct bcache_buf* b);

// Release a locked buffer
void brelse(struct bcache_buf* b);

void bpin(struct bcache_buf* b);
void bunpin(struct bcache_buf* b);

void bcache_init();
