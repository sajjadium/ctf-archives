#include <pthread.h>

#include "buf_cache.h"
#include "util.h"
#include "block_device.h"
#include "assert.h"
#include "sys/time.h"

struct bcache_hashtbl {
  pthread_spinlock_t lock;
  struct bcache_buf head;
};

struct bcache {
  struct bcache_buf buf[NCACHE_BUF];

  pthread_mutex_t lock;

  struct bcache_hashtbl hash[BCACHE_HASH_SIZE];
};

static struct bcache bcache;

void bcache_init() {
  struct bcache_buf* b;

  for (int i = 0; i < BCACHE_HASH_SIZE; i++) {
    pthread_spin_init(&bcache.hash[i].lock, PTHREAD_PROCESS_SHARED);
    bcache.hash[i].head.prev = &bcache.hash[i].head;
    bcache.hash[i].head.next = &bcache.hash[i].head;
  }

  // add all buffers to hash[0]
  for (b = bcache.buf; b < bcache.buf + NCACHE_BUF; b++) {
    b->next = bcache.hash[0].head.next;
    b->prev = &bcache.hash[0].head;
    pthread_mutex_init(&b->lock, NULL);
    bcache.hash[0].head.next->prev = b;
    bcache.hash[0].head.next       = b;
  }
}

static uint bcache_hash(uint blockno) { return blockno % BCACHE_HASH_SIZE; }

static struct bcache_buf* bget(uint blockno) {
  struct bcache_buf* b;

  int hashid                    = bcache_hash(blockno);
  struct bcache_hashtbl* bucket = &bcache.hash[hashid];
  pthread_spin_lock(&bucket->lock);

  for (b = bucket->head.next; b != &bucket->head; b = b->next) {
#ifdef DEBUG
    assert(bcache_hash(b->blockno) == hashid);
#endif
    if (b->blockno == blockno) {
      b->refcnt++;
      pthread_spin_unlock(&bucket->lock);
      pthread_mutex_lock(&b->lock);
      return b;
    }
  }

  // Not cached.
  // Recycle per hashtbl and get the least recent buf

  struct bcache_buf* least_recent_buf = 0;
  for (b = bcache.hash[hashid].head.prev; b != &bcache.hash[hashid].head;
       b = b->prev) {
    uint64_t least_recent_time_stamp = 0;
    least_recent_time_stamp--;
    if (b->refcnt == 0) {
      if (b->timestamp <= least_recent_time_stamp) {
        least_recent_buf        = b;
        least_recent_time_stamp = b->timestamp;
      }
    }

    if (least_recent_buf) {
      b          = least_recent_buf;
      b->blockno = blockno;
      b->refcnt  = 1;
      b->valid   = 0;
      pthread_spin_unlock(&bucket->lock);
      pthread_mutex_lock(&b->lock);
      return b;
    }
  }

  int hidx;
  while (1) {
    for (hidx = 0; hidx < BCACHE_HASH_SIZE; hidx++) {
      if (hidx == hashid) {
        continue;
      }
      uint64_t least_recent_time_stamp = 0;
      least_recent_time_stamp--;

      pthread_spin_lock(&bcache.hash[hidx].lock);
      for (b = bcache.hash[hidx].head.prev; b != &bcache.hash[hidx].head;
           b = b->prev) {
        if (b->refcnt == 0) {
          if (b->timestamp <= least_recent_time_stamp) {
            least_recent_buf        = b;
            least_recent_time_stamp = b->timestamp;
          }
        }
      }
      if (least_recent_buf) {
        break;
      }
      pthread_spin_unlock(&bcache.hash[hidx].lock);
    }

    if (least_recent_buf == 0) {
      myfuse_debug_log("bget: no buffers, find again..");
    } else {
      break;
    }
  }

  b          = least_recent_buf;
  b->blockno = blockno;
  b->valid   = 0;
  b->refcnt  = 1;
  // unlink
  b->next->prev = b->prev;
  b->prev->next = b->next;
  pthread_spin_unlock(&bcache.hash[hidx].lock);

  // link
  b->next                 = bucket->head.next;
  b->prev                 = &bucket->head;
  bucket->head.next->prev = b;
  bucket->head.next       = b;
  pthread_spin_unlock(&bucket->lock);

  pthread_mutex_lock(&b->lock);

  return b;
}

struct bcache_buf* bread(uint blockno) {
  struct bcache_buf* b;

  b = bget(blockno);
  if (!b->valid) {
    read_block_raw(blockno, b->data);
    b->valid = 1;
  }
  return b;
}

int bwrite(struct bcache_buf* b) {
  DEBUG_TEST(if (!pthread_mutex_trylock(&b->lock)) {
    err_exit("bwrite called with unlocked buf");
  });

  return write_block_raw(b->blockno, b->data);
}

static inline uint64_t current_timestamp() {
  struct timeval te;
  gettimeofday(&te, NULL);  // get current time
  long long milliseconds =
      te.tv_sec * 100LL + te.tv_usec / 100;  // calculate milliseconds
  return milliseconds;
}

void brelse(struct bcache_buf* b) {
  DEBUG_TEST(if (!pthread_mutex_trylock(&b->lock)) {
    err_exit("brelse called with unlocked buf");
  });

  pthread_mutex_unlock(&b->lock);
  int hashid                    = bcache_hash(b->blockno);
  struct bcache_hashtbl* bucket = &bcache.hash[hashid];
  pthread_spin_lock(&bucket->lock);

  b->refcnt--;
  if (b->refcnt == 0) {
    // no one is waiting for it.
    // update timestamp
    b->timestamp = current_timestamp();
  }

  pthread_spin_unlock(&bucket->lock);
}

void bpin(struct bcache_buf* b) {
  int hashid                    = bcache_hash(b->blockno);
  struct bcache_hashtbl* bucket = &bcache.hash[hashid];
  pthread_spin_lock(&bucket->lock);
  b->refcnt++;
  pthread_spin_unlock(&bucket->lock);
}

void bunpin(struct bcache_buf* b) {
  int hashid                    = bcache_hash(b->blockno);
  struct bcache_hashtbl* bucket = &bcache.hash[hashid];
  pthread_spin_lock(&bucket->lock);
  b->refcnt--;
  pthread_spin_unlock(&bucket->lock);
}
