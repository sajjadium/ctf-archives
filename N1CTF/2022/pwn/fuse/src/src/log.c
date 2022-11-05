#include "log.h"
#include "buf_cache.h"
#include <pthread.h>

// Contents of the header block, used for both the on-disk header block
// and to keep track in memory of logged block# before commit.
struct fslogheader {
  int n;
  int block[NLOG];
};

// log's in memory representation
struct fslog {
  pthread_mutex_t lock;
  int start;
  int size;
  int outstanding;  // how many FS sys calls are executing
  int committing;   // in commit(), please wait
  struct fslogheader lh;
  pthread_cond_t wakeup;  // for the pthread_cond_wait
};

struct fslog fslog;

static void recover_from_log();
static void commit();

void log_init(struct superblock* sb) {
  if (sizeof(struct fslogheader) > BSIZE) {
    err_exit("log_init: too big logheader");
  }

  pthread_mutex_init(&fslog.lock, NULL);
  fslog.start = sb->logstart;
  fslog.size  = sb->nlog;
  pthread_cond_init(&fslog.wakeup, NULL);
  recover_from_log();
}

static void install_transaction(int recovering) {
  for (int tail = 0; tail < fslog.lh.n; tail++) {
    struct bcache_buf* log_buf =
        bread(fslog.start + tail + 1);                         // read log block
    struct bcache_buf* dst_buf = bread(fslog.lh.block[tail]);  // read dst
    memcpy(dst_buf->data, log_buf->data, BSIZE);
    bwrite(dst_buf);
    if (recovering == 0) {
      bunpin(dst_buf);
    }
    brelse(log_buf);
    brelse(dst_buf);
  }
}

static void read_log_header_from_disk() {
  struct bcache_buf* buf = bread(fslog.start);
  struct fslogheader* lh = (struct fslogheader*)(buf->data);

  fslog.lh.n = lh->n;
  for (int i = 0; i < fslog.lh.n; i++) {
    fslog.lh.block[i] = lh->block[i];
  }
  brelse(buf);
}

static void write_log_header_to_disk() {
  struct bcache_buf* buf = bread(fslog.start);
  struct fslogheader* lh = (struct fslogheader*)(buf->data);

  lh->n = fslog.lh.n;
  for (int i = 0; i < fslog.lh.n; i++) {
    lh->block[i] = fslog.lh.block[i];
  }
  bwrite(buf);
  brelse(buf);
}

static void recover_from_log() {
  read_log_header_from_disk();
  install_transaction(1);
  fslog.lh.n = 0;
  write_log_header_to_disk();
}

// called at the start of each FS system call
void begin_op() {
  pthread_mutex_lock(&fslog.lock);
  while (1) {
    if (fslog.committing) {
      pthread_cond_wait(&fslog.wakeup, &fslog.lock);
    } else if (fslog.lh.n + (fslog.outstanding + 1) * MAXOPBLOCKS > NLOG) {
      pthread_cond_wait(&fslog.wakeup, &fslog.lock);
    } else {
      fslog.outstanding++;
      pthread_mutex_unlock(&fslog.lock);
      break;
    }
  }
  n_log_wrote = 0;
}

void end_op() {
  int do_commit = 0;

  pthread_mutex_lock(&fslog.lock);
  fslog.outstanding -= 1;
  if (fslog.committing) {
    err_exit("log.committing");
  }
  if (fslog.outstanding == 0) {
    do_commit        = 1;
    fslog.committing = 1;
  } else {
    // begin_op() may be waiting for log space,
    // and decrementing log.outstanding has decreased
    // the amount of reserved space.
    pthread_cond_broadcast(&fslog.wakeup);
  }
  pthread_mutex_unlock(&fslog.lock);

  if (do_commit) {
    // call commit w/o holding locks, since not allowed
    // to sleep with locks.
    commit();
    pthread_mutex_lock(&fslog.lock);
    fslog.committing = 0;
    pthread_cond_broadcast(&fslog.wakeup);
    pthread_mutex_unlock(&fslog.lock);
  }
}

static void write_from_cache_to_log() {
  for (int tail = 0; tail < fslog.lh.n; tail++) {
    struct bcache_buf* to   = bread(fslog.start + tail + 1);
    struct bcache_buf* from = bread(fslog.lh.block[tail]);
    memmove(to->data, from->data, BSIZE);
    bwrite(to);
    brelse(to);
    brelse(from);
  }
}

static void commit() {
  if (fslog.lh.n > 0) {
    write_from_cache_to_log();
    write_log_header_to_disk();
    install_transaction(0);
    fslog.lh.n = 0;
    write_log_header_to_disk();
  }
}

// use this dark magic to make higher level need not to worry about the limit of
// MAXOPBLOCK
uint __thread n_log_wrote = 0;

void logged_write(struct bcache_buf* b) {
  pthread_mutex_lock(&fslog.lock);
  if (fslog.lh.n >= NLOG || fslog.lh.n >= fslog.size - 1) {
    err_exit("too big a transaction");
  }
  if (fslog.outstanding < 1) {
    err_exit("logged_write outside of transaction");
  }

  n_log_wrote++;

  int block_idx;
  for (block_idx = 0; block_idx < fslog.lh.n; block_idx++) {
    if (fslog.lh.block[block_idx] == b->blockno) {
      break;  // write to the same block in the log
    }
  }
  fslog.lh.block[block_idx] = b->blockno;
  if (block_idx == fslog.lh.n) {
    bpin(b);
    fslog.lh.n++;
  }
  pthread_mutex_unlock(&fslog.lock);
}

struct bcache_buf* logged_read(uint blockno) {
  return bread(blockno);
}

void logged_relse(struct bcache_buf* b) { brelse(b); }
