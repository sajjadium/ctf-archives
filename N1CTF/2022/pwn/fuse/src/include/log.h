#pragma once
#include "param.h"
#include "buf_cache.h"

// Simple logging that allows concurrent FS system calls.
//
// A log transaction contains the updates of multiple FS system
// calls. The logging system only commits when there are
// no FS system calls active. Thus there is never
// any reasoning required about whether a commit might
// write an uncommitted system call's updates to disk.
//
// A system call should call begin_op()/end_op() to mark
// its start and end. Usually begin_op() just increments
// the count of in-progress FS system calls and returns.
// But if it thinks the log is close to running out, it
// sleeps until the last outstanding end_op() commits.
//
// the log layout on device is
// |    header block   | # containing blockno for following blocks
// | block A's content |
// | block B's content |
// | block C's content |
// |        ...        |
//
// take this log system as do operation first on disk's log section, then on the
// real place;

void log_init(struct superblock* sb);

// loged_write will not really write to the disk.
// commit()/write_log() will do the real write.
//
// loged_write() and loged_read() replaces bread() and bwrite()
//   bp = loged_read()
//   modify bp->data[]
//   loged_write(bp)
//   loged_relse(bp)
//
void logged_write(struct bcache_buf* b);

// this is a wrapper to bread() to make the interface consistent
struct bcache_buf* logged_read(uint blockno);

// this is a wrapper to brelse() to make the interface consistent
void logged_relse(struct bcache_buf* b);

void begin_op();
void end_op();

extern uint __thread n_log_wrote;
