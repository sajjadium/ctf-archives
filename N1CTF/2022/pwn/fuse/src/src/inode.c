#include "inode.h"
#include <pthread.h>
#include <malloc.h>
#include <assert.h>
#include <errno.h>
#include "log.h"
#include "block_allocator.h"

struct {
  pthread_spinlock_t lock;
  size_t ninode;
  struct inode** inode;
} itable;

pthread_mutex_t ialloc_lock;

int inode_init(struct superblock* sb) {
  pthread_spin_init(&itable.lock, PTHREAD_PROCESS_SHARED);
#define NINODE_INIT 30
  itable.ninode = NINODE_INIT;
  itable.inode  = malloc(sizeof(struct inode*) * NINODE_INIT);
  for (int i = 0; i < NINODE_INIT; i++) {
    itable.inode[i] = calloc(1, sizeof(struct inode));
    pthread_mutex_init(&itable.inode[i]->lock, NULL);
  }

  pthread_mutex_init(&ialloc_lock, NULL);

  memset(&bmap_cache, 0, sizeof(bmap_cache));
  block_allocator_refresh(sb);
  return 0;
}

static void itable_grow() {
  myfuse_debug_log("itable_grow: %d -> %d", itable.ninode, itable.ninode * 2);
  if (!pthread_spin_trylock(&itable.lock)) {
    err_exit("itable_grow called not within itable locked");
  }
  itable.inode =
      realloc(itable.inode, sizeof(struct inode*) * itable.ninode * 2);
  itable.ninode *= 2;
  for (int i = itable.ninode / 2; i < itable.ninode; i++) {
    itable.inode[i] = calloc(1, sizeof(struct inode));
    pthread_mutex_init(&itable.inode[i]->lock, NULL);
  }
}

// return the {inum}-th inode's in memory copy
// the inode isn't locked and haven't read from disk
struct inode* iget(uint inum) {
  struct inode* empty_victim = 0;
  pthread_spin_lock(&itable.lock);
  int n = itable.ninode;
  for (int i = 0; i < n; i++) {
    struct inode* ip = itable.inode[i];
    if (ip == NULL || (size_t)ip & 1) {
      // odd, this shouldn't happen
      myfuse_nonfatal("itable corrupt");
      break;
    }
    if (ip->inum == inum && ip->ref > 0) {
      ip->ref++;
      pthread_spin_unlock(&itable.lock);
      return ip;
    }
    if (ip->ref == 0 && empty_victim == 0) {
      empty_victim = ip;
    }
  }

  if (empty_victim != 0) {
    empty_victim->inum  = inum;
    empty_victim->ref   = 1;
    empty_victim->valid = 0;
    pthread_spin_unlock(&itable.lock);
    return empty_victim;
  }
  // reach here, means the inode cache is too small
  itable_grow();
  pthread_spin_unlock(&itable.lock);
  return iget(inum);
}

// currently only type FILE && DIR is allowed
struct inode* ialloc(short type) {
  struct bcache_buf* bp;
  struct dinode* dip;

  for (int inum = 1; inum < MYFUSE_STATE->sb.ninodes; inum++) {
    bp  = logged_read(IBLOCK(inum));
    dip = (struct dinode*)bp->data + inum % IPB;
    if (dip->type == T_UNUSE_INODE_MYFUSE) {
      memset(dip, 0, sizeof(*dip));
      dip->type = type;
      logged_write(bp);
      logged_relse(bp);
      return iget(inum);
    }
    logged_relse(bp);
  }

  // no on disk inodes avaliable
  // too much file, for simple, this can't be recover
  // shut the file system down
  err_exit("too much file on disk!");
  return NULL;
}

// Increment reference count for ip.
// Returns ip to enable ip = idup(ip1) idiom.
struct inode* idup(struct inode* ip) {
  pthread_spin_lock(&itable.lock);
  ip->ref++;
  pthread_spin_unlock(&itable.lock);
  return ip;
}

// Lock the given inode
// Read the inode from disk if necessary
void ilock(struct inode* ip) {
  if (ip == 0 || ip->ref < 1) {
    err_exit("ilock got invalid inode");
  }

  pthread_mutex_lock(&ip->lock);

  if (!ip->valid) {
    // read from disk
    struct bcache_buf* bp = logged_read(IBLOCK(ip->inum));
    struct dinode* dip    = (struct dinode*)bp->data + ip->inum % IPB;

    ip->type         = dip->type;
    ip->major        = dip->major;
    ip->minor        = dip->minor;
    ip->nlink        = dip->nlink;
    ip->size         = dip->size;
    ip->perm         = dip->perm;
    ip->st_atimespec = dip->st_atimespec;
    ip->st_mtimespec = dip->st_mtimespec;
    ip->st_ctimespec = dip->st_ctimespec;
    memmove(ip->addrs, dip->addrs, sizeof(ip->addrs));
    logged_relse(bp);
    ip->valid = 1;
    if (ip->type == T_UNUSE_INODE_MYFUSE) {
      err_exit("ilock: ip is unused");
    }

    if (ip->type != T_FILE_INODE_MYFUSE && ip->type != T_DIR_INODE_MYFUSE &&
        ip->type != T_DEVICE_INODE_MYFUSE) {
      err_exit("ilock: ip has invalid type");
    }
  }
}

void iunlock(struct inode* ip) {
  DEBUG_TEST(
      // pthread_mutex_trylock: return 0 if not locked
      if (ip == 0 || !pthread_mutex_trylock(&ip->lock) || ip->ref < 1) {
        err_exit("iunlock: got invalid inode");
      });

  pthread_mutex_unlock(&ip->lock);
}

// Copy a modified in-memory inode to disk.
// Must be called after every change to an ip->xxx field
// that lives on disk.
// Caller must hold ip->lock.
void iupdate(struct inode* ip) {
  struct bcache_buf* bp;
  struct dinode* dip;

  bp                = logged_read(IBLOCK(ip->inum));
  dip               = (struct dinode*)bp->data + ip->inum % IPB;
  dip->type         = ip->type;
  dip->major        = ip->major;
  dip->minor        = ip->minor;
  dip->nlink        = ip->nlink;
  dip->size         = ip->size;
  dip->perm         = ip->perm;
  dip->st_atimespec = ip->st_atimespec;
  dip->st_mtimespec = ip->st_mtimespec;
  get_current_timespec(&ip->st_ctimespec);
  dip->st_ctimespec = ip->st_ctimespec;
  memmove(dip->addrs, ip->addrs, sizeof(ip->addrs));
  logged_write(bp);
  logged_relse(bp);
}
void itrunc(struct inode* ip);

// Drop a reference to an in-memory inode.
// If that was the last reference, the inode table entry can
// be recycled.
// If that was the last reference and the inode has no links
// to it, free the inode (and its content) on disk.
// All calls to iput() must be inside a transaction in
// case it has to free the inode.
void iput(struct inode* ip) {
  pthread_spin_lock(&itable.lock);

  if (ip->ref == 1 && ip->valid && ip->nlink == 0) {
    // truncate and free

    pthread_mutex_lock(&ip->lock);

    pthread_spin_unlock(&itable.lock);

    itrunc(ip);
    ip->type = T_UNUSE_INODE_MYFUSE;
    iupdate(ip);
    ip->valid = 0;
    pthread_mutex_unlock(&ip->lock);
    pthread_spin_lock(&itable.lock);
  }
  ip->ref--;
  pthread_spin_unlock(&itable.lock);
}

void iunlockput(struct inode* ip) {
  iunlock(ip);
  iput(ip);
}

static inline void assert_no_need_to_restart_op_in_imap2blockno() {
  if (n_log_wrote >= MAXOPBLOCKS - 1 - 3) {
    err_exit("too many blocks in one op");
  }
}

// Inode content
//
// The content (data) associated with each inode is stored
// in blocks on the disk. The first NDIRECT block numbers
// are listed in ip->addrs[].  The next NINDIRECT blocks are
// listed in block ip->addrs[NDIRECT]...
// there is total 3 indirect blocks

// Return the disk block address of the nth block in inode ip.
// If there is no such block, bmap allocates one.

uint imap2blockno(struct inode* ip, uint bn) {
  assert_no_need_to_restart_op_in_imap2blockno();

  uint addr, *a;
  struct bcache_buf* bp;

  if (bn < NDIRECT) {
    if ((addr = ip->addrs[bn]) == 0) {
      ip->addrs[bn] = addr = block_alloc();
    }
    return addr;
  }
  bn -= NDIRECT;

  // 1st indirect block
  // [d d .. d i i i]
  //           |
  //           +---> [d d .. d]
  if (bn < NINDIRECT1) {
    // Load indirect block, allocating if necessary.
    if ((addr = ip->addrs[NDIRECT]) == 0) {
      ip->addrs[NDIRECT] = addr = block_alloc();
    }
    bp = logged_read(addr);
    a  = (uint*)bp->data;
    if ((addr = a[bn]) == 0) {
      a[bn] = addr = block_alloc();
      logged_write(bp);
    }
    logged_relse(bp);
    return addr;
  }
  bn -= NINDIRECT1;

  // 2st indirect block
  // [d d .. d i i i]
  //             |
  //             +---> [i i .. i]
  //                    | |
  //     [d d .. d] <---+ +---> [d d .. d]
  if (bn < NINDIRECT2) {
    uint entry  = bn / NINDIRECT1;
    uint offset = bn % NINDIRECT1;
    // Load indirect entry, allocating if necessary
    if ((addr = ip->addrs[NDIRECT + 1]) == 0) {
      ip->addrs[NDIRECT + 1] = addr = block_alloc();
    }
    bp = logged_read(addr);
    a  = (uint*)bp->data;
    assert(entry * sizeof(uint) < BSIZE);
    if ((addr = a[entry]) == 0) {
      a[entry] = addr = block_alloc();
      logged_write(bp);
    }
    logged_relse(bp);

    bp = logged_read(addr);
    a  = (uint*)bp->data;
    if ((addr = a[offset]) == 0) {
      a[offset] = addr = block_alloc();
      logged_write(bp);
    }
    logged_relse(bp);
    return addr;
  }
  bn -= NINDIRECT2;

  // 3st indirect block
  // [d d .. d i i i]
  //             |
  //             +---> [i i .. i]
  //                    | |
  //     [i i .. i] <---+ +---> [i i .. i]
  //      |
  //      +---> [d d .. d]
  if (bn < NINDIRECT3) {
    uint entryl1  = bn / NINDIRECT2;
    uint offsetl1 = bn % NINDIRECT2;
    uint entryl2  = offsetl1 / NINDIRECT1;
    uint offsetl2 = offsetl1 % NINDIRECT1;
    // Load indirect entry, allocating if necessary
    if ((addr = ip->addrs[NDIRECT + 2]) == 0) {
      ip->addrs[NDIRECT + 2] = addr = block_alloc();
    }
    bp = logged_read(addr);
    a  = (uint*)bp->data;
    assert(entryl1 * sizeof(uint) < BSIZE);
    if ((addr = a[entryl1]) == 0) {
      a[entryl1] = addr = block_alloc();
      logged_write(bp);
    }
    logged_relse(bp);

    bp = logged_read(addr);
    a  = (uint*)bp->data;
    assert(entryl2 * sizeof(uint) < BSIZE);
    if ((addr = a[entryl2]) == 0) {
      a[entryl2] = addr = block_alloc();
      logged_write(bp);
    }
    logged_relse(bp);

    bp = logged_read(addr);
    a  = (uint*)bp->data;
    if ((addr = a[offsetl2]) == 0) {
      a[offsetl2] = addr = block_alloc();
      logged_write(bp);
    }
    logged_relse(bp);
    return addr;
  }

  err_exit("imap2blockno: inode too big");
  return -1;
}

void itrunc(struct inode* ip) {
  myfuse_debug_log("itrunc");
  for (int i = 0; i < NDIRECT; i++) {
    if (ip->addrs[i]) {
      block_free(ip->addrs[i]);
    }
  }

  if (ip->addrs[NDIRECT]) {
    struct bcache_buf* bp = logged_read(ip->addrs[NDIRECT]);
    uint* a               = (uint*)bp->data;
    for (int i = 0; i < NINDIRECT1; i++) {
      if (a[i]) {
        block_free(a[i]);
      }
    }
    logged_relse(bp);
    block_free(ip->addrs[NDIRECT]);
  }

  if (ip->addrs[NDIRECT + 1]) {
    struct bcache_buf* bp = logged_read(ip->addrs[NDIRECT + 1]);
    uint* a               = (uint*)bp->data;
    for (int i = 0; i < NINDIRECT1; i++) {
      if (a[i]) {
        struct bcache_buf* bp2 = logged_read(a[i]);
        uint* a2               = (uint*)bp2->data;
        for (int j = 0; j < NINDIRECT1; j++) {
          if (a2[j]) {
            block_free(a2[j]);
          }
        }
        logged_relse(bp2);
        block_free(a[i]);
      }
    }
    logged_relse(bp);
    block_free(ip->addrs[NDIRECT + 1]);
  }

  if (ip->addrs[NDIRECT + 2]) {
    struct bcache_buf* bp = logged_read(ip->addrs[NDIRECT + 2]);
    uint* a               = (uint*)bp->data;
    for (int i = 0; i < NINDIRECT1; i++) {
      if (a[i]) {
        struct bcache_buf* bp2 = logged_read(a[i]);
        uint* a2               = (uint*)bp2->data;
        for (int j = 0; j < NINDIRECT1; j++) {
          if (a2[j]) {
            struct bcache_buf* bp3 = logged_read(a2[j]);
            uint* a3               = (uint*)bp3->data;
            for (int k = 0; k < NINDIRECT1; k++) {
              if (a3[k]) {
                block_free(a3[k]);
              }
            }
            logged_relse(bp3);
            block_free(a2[j]);
          }
        }
        logged_relse(bp2);
        block_free(a[i]);
      }
    }
    logged_relse(bp);
    block_free(ip->addrs[NDIRECT + 2]);
  }

  // TODO: this is unneccessary?
  memset(ip->addrs, 0, sizeof(ip->addrs));

  ip->size = 0;
  iupdate(ip);
}

void itrunc2size_log_op_restart_helper() {
  if (n_log_wrote >= MAXOPBLOCKS - 1 - 3) {
    end_op();
    begin_op();
  }
}

#define block_free_safe(x)             \
  itrunc2size_log_op_restart_helper(); \
  block_free((x));                     \
  (x) = 0;

void imap2blockno_free(struct inode* ip, uint bn) {
  assert_no_need_to_restart_op_in_imap2blockno();

  uint addr, *a;
  struct bcache_buf* bp;

  if (bn < NDIRECT) {
    if ((addr = ip->addrs[bn]) != 0) {
      block_free_safe(ip->addrs[bn]);
    }
    return;
  }
  bn -= NDIRECT;

  // 1st indirect block
  // [d d .. d i i i]
  //           |
  //           +---> [d d .. d]
  if (bn < NINDIRECT1) {
    // Load indirect block, allocating if necessary.
    if ((addr = ip->addrs[NDIRECT]) == 0) {
      return;
    }
    bp = logged_read(addr);
    a  = (uint*)bp->data;
    if ((addr = a[bn]) != 0) {
      block_free_safe(a[bn]);
      logged_write(bp);
    }
    logged_relse(bp);
    return;
  }
  bn -= NINDIRECT1;

  // 2st indirect block
  // [d d .. d i i i]
  //             |
  //             +---> [i i .. i]
  //                    | |
  //     [d d .. d] <---+ +---> [d d .. d]
  if (bn < NINDIRECT2) {
    uint entry  = bn / NINDIRECT1;
    uint offset = bn % NINDIRECT1;
    // Load indirect entry, allocating if necessary
    if ((addr = ip->addrs[NDIRECT + 1]) == 0) {
      ip->addrs[NDIRECT + 1] = addr = block_alloc();
    }
    bp = logged_read(addr);
    a  = (uint*)bp->data;
    assert(entry * sizeof(uint) < BSIZE);
    if ((addr = a[entry]) == 0) {
      logged_relse(bp);
      return;
    }
    logged_relse(bp);

    bp = logged_read(addr);
    a  = (uint*)bp->data;
    if ((addr = a[offset]) != 0) {
      block_free_safe(a[offset]);
      logged_write(bp);
    }
    logged_relse(bp);
    return;
  }
  bn -= NINDIRECT2;

  // 3st indirect block
  // [d d .. d i i i]
  //             |
  //             +---> [i i .. i]
  //                    | |
  //     [i i .. i] <---+ +---> [i i .. i]
  //      |
  //      +---> [d d .. d]
  if (bn < NINDIRECT3) {
    uint entryl1  = bn / NINDIRECT2;
    uint offsetl1 = bn % NINDIRECT2;
    uint entryl2  = offsetl1 / NINDIRECT1;
    uint offsetl2 = offsetl1 % NINDIRECT1;
    // Load indirect entry, allocating if necessary
    if ((addr = ip->addrs[NDIRECT + 2]) == 0) {
      // exit
      return;
    }
    bp = logged_read(addr);
    a  = (uint*)bp->data;
    assert(entryl1 * sizeof(uint) < BSIZE);
    if ((addr = a[entryl1]) == 0) {
      logged_relse(bp);
      return;
    }
    logged_relse(bp);

    bp = logged_read(addr);
    a  = (uint*)bp->data;
    assert(entryl2 * sizeof(uint) < BSIZE);
    if ((addr = a[entryl2]) == 0) {
      logged_relse(bp);
      return;
    }
    logged_relse(bp);

    bp = logged_read(addr);
    a  = (uint*)bp->data;
    if ((addr = a[offsetl2]) != 0) {
      block_free_safe(a[offsetl2]);
      logged_write(bp);
    }
    logged_relse(bp);
    return;
  }

  err_exit("imap2blockno_free: inode too big");
  return;
}

// called inside op and lock
int itrunc2size(struct inode* ip, size_t size) {
  DEBUG_TEST(if (ip->type != T_FILE_INODE_MYFUSE) {
    err_exit("itrunc2size called on non-file inode");
  });

  if (size == ip->size) {
    goto out;
  }

  if (size == 0) {
    itrunc(ip);
  }

  size_t nbytes_aligned    = 0;
  nbytes_aligned           = ROUNDUP(size, BSIZE);
  long long target_blockno = nbytes_aligned / BSIZE;
  long long origin_blockno = ROUNDUP(ip->size, BSIZE) / BSIZE;
  myfuse_debug_log("%lx truncate to %lx, %lx", ip->size, size, nbytes_aligned);

  if (target_blockno >= origin_blockno) {
    for (uint i = origin_blockno; i < target_blockno; i++) {
      // alloc the node
      itrunc2size_log_op_restart_helper();
      (void)imap2blockno(ip, i);
    }
  } else {
    for (uint i = target_blockno; i < origin_blockno; i++) {
      itrunc2size_log_op_restart_helper();
      imap2blockno_free(ip, i);
    }
  }

out:
  ip->size = size;
  iupdate(ip);

  return 0;
}
#undef block_free

static size_t min(size_t a, size_t b) { return a < b ? a : b; }

static void restart_op_on(struct inode* ip, uint nwrote) {
  // iupdate will write the inode to disk, so we need to
  // reserve the op
  if (n_log_wrote >= nwrote - 1) {
    iupdate(ip);
    iunlock(ip);
    end_op();
    begin_op();
    ilock(ip);
  }
}

long inode_write_nbytes_locked(struct inode* ip, const char* data,
                               size_t nbytes, size_t off) {
  if (off > MAXFILE_SIZE) {
    return 0;
  }

  if (off + nbytes > MAXFILE_SIZE) {
    nbytes -= (off + nbytes - MAXFILE_SIZE);
  }

  long n_write = nbytes;

  // update size
  ip->size = ip->size < off + nbytes ? off + nbytes : ip->size;
  iupdate(ip);

  uint inode_block_start = ((size_t)(off / BSIZE));
  size_t from_start      = off % BSIZE;
  size_t n_left          = BSIZE - from_start;
  restart_op_on(ip, MAXOPBLOCKS - 1 - 3 - 1);
  struct bcache_buf* bp = logged_read(imap2blockno(ip, inode_block_start));
  memmove(bp->data + from_start, data, min(n_left, nbytes));
  logged_write(bp);
  logged_relse(bp);
  if (nbytes <= n_left) {
    get_current_timespec(&ip->st_atimespec);
    ip->st_mtimespec = ip->st_atimespec;
    iupdate(ip);
    return nbytes;
  }
  nbytes -= n_left;
  data += n_left;

  // start block write
  uint inode_blockno = inode_block_start + 1;
  for (; nbytes > BSIZE; nbytes -= BSIZE) {
    // 3 is the max imap2blockno will write
    // 1 is the followed write
    restart_op_on(ip, MAXOPBLOCKS - 1 - 3 - 1);

    bp = logged_read(imap2blockno(ip, inode_blockno));
    memmove(bp->data, data, BSIZE);
    logged_write(bp);
    logged_relse(bp);

    data += BSIZE;
    inode_blockno++;
  }

  // 3 is the max imap2blockno will write
  // 1 is the followed write
  restart_op_on(ip, MAXOPBLOCKS - 3 - 1);

  // write last block
  if (nbytes) {
    bp = logged_read(imap2blockno(ip, inode_blockno));
    memmove(bp->data, data, nbytes);
    logged_write(bp);
    logged_relse(bp);
  }

  get_current_timespec(&ip->st_atimespec);
  ip->st_mtimespec = ip->st_atimespec;
  iupdate(ip);
  return n_write;
}

long inode_read_nbytes_locked(struct inode* ip, char* data, size_t nbytes,
                              size_t off) {
  if (off > ip->size) {
    return 0;
  }

  if (off + nbytes > ip->size) {
    nbytes -= (off + nbytes - ip->size);
  }
  size_t n_read = nbytes;

  uint inode_block_start = ((size_t)(off / BSIZE));
  size_t from_start      = off % BSIZE;
  size_t n_left          = BSIZE - from_start;
  struct bcache_buf* bp  = logged_read(imap2blockno(ip, inode_block_start));
  memmove(data, bp->data + from_start, min(n_left, nbytes));
  logged_relse(bp);
  if (nbytes <= n_left) {
    get_current_timespec(&ip->st_atimespec);
    iupdate(ip);
    return nbytes;
  }
  nbytes -= n_left;
  data += n_left;

  // start block write
  uint inode_blockno = inode_block_start + 1;
  for (; nbytes > BSIZE; nbytes -= BSIZE) {
    // 3 is the max imap2blockno will write
    restart_op_on(ip, MAXOPBLOCKS - 1 - 3);

    bp = logged_read(imap2blockno(ip, inode_blockno));
    memmove(data, bp->data, BSIZE);
    logged_relse(bp);
    data += BSIZE;
    inode_blockno++;
  }

  // read last block
  if (nbytes) {
    // 3 is the max imap2blockno will write
    restart_op_on(ip, MAXOPBLOCKS - 1 - 3);
    bp = logged_read(imap2blockno(ip, inode_blockno));
    memmove(data, bp->data, nbytes);
    logged_relse(bp);
  }
  iupdate(ip);

  get_current_timespec(&ip->st_atimespec);
  return n_read;
}

long inode_write_nbytes_unlocked(struct inode* ip, const char* data,
                                 size_t bytes, size_t off) {
  begin_op();
  ilock(ip);
  long nbytes = inode_write_nbytes_locked(ip, data, bytes, off);
  iunlock(ip);
  end_op();
  return nbytes;
}

long inode_read_nbytes_unlocked(struct inode* ip, char* data, size_t bytes,
                                size_t off) {
  begin_op();
  ilock(ip);
  long nbytes = inode_read_nbytes_locked(ip, data, bytes, off);
  iunlock(ip);
  end_op();
  return nbytes;
}

int stat_inode(struct inode* ip, struct stat* st) {
  int res        = 0;
  st->st_nlink   = ip->nlink;
  st->st_size    = ip->size;
  st->st_ino     = ip->inum;
  st->st_blksize = BSIZE;
  st->st_atim    = ip->st_atimespec;
  st->st_ctim    = ip->st_ctimespec;
  st->st_mtim    = ip->st_mtimespec;
  switch (ip->type) {
    case T_DIR_INODE_MYFUSE:
      st->st_mode = S_IFDIR | ip->perm;
      break;
    case T_FILE_INODE_MYFUSE:
      st->st_mode = S_IFREG | ip->perm;
      break;
    case T_DEVICE_INODE_MYFUSE:
      myfuse_debug_log("`inum %d' is device, not supported", ip->inum);
      res = -ENOENT;
      break;
    default:
      myfuse_debug_log("inum `%d' has unknow type", ip->inum);
      res = -ENOENT;
      break;
  }
  return res;
}

int stat_inum(uint inum, struct stat* st) {
  struct inode* ip = iget(inum);
  ilock(ip);
  int res = stat_inode(ip, st);
  iunlockput(ip);
  return res;
}
