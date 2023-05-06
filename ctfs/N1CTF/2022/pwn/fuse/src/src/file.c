#include "file.h"
#include "inode.h"
#include "directory.h"
#include <stddef.h>
#include <fcntl.h>
#include <errno.h>
#include <assert.h>
#include <linux/fs.h>
#include "log.h"

#define NFILE_INIT 50

struct ftable {
  pthread_spinlock_t lock;
  struct file **files;
  uint nfile;
} ftable;

void ftable_grow() {
  ftable.files =
      realloc(ftable.files, 2 * ftable.nfile * sizeof(struct file *));
  ftable.nfile *= 2;
  for (int i = ftable.nfile / 2; i < ftable.nfile; i++) {
    ftable.files[i] = calloc(1, sizeof(struct file));
  }
}

void file_init() {
  ftable.files = malloc(sizeof(struct file *) * NFILE_INIT);
  ftable.nfile = NFILE_INIT;
  pthread_spin_init(&ftable.lock, PTHREAD_PROCESS_SHARED);
  for (int i = 0; i < ftable.nfile; i++) {
    ftable.files[i] = calloc(1, sizeof(struct file));
  }
}

struct file *filealloc() {
  struct file *f;
  pthread_spin_lock(&ftable.lock);
  for (int i = 0; i < ftable.nfile; i++) {
    if (ftable.files[i]->ref == 0) {
      f      = ftable.files[i];
      f->ref = 1;
      pthread_spin_unlock(&ftable.lock);
      return f;
    }
  }
  ftable_grow();
  f      = ftable.files[ftable.nfile / 2];
  f->ref = 1;
  pthread_spin_unlock(&ftable.lock);
  return f;
}

struct file *filedup(struct file *f) {
  pthread_spin_lock(&ftable.lock);
  if (f->ref < 1) {
    err_exit("filedup: ref < 1");
  };
  f->ref++;
  pthread_spin_unlock(&ftable.lock);
  return f;
}

void fileclose(struct file *f) {
  pthread_spin_lock(&ftable.lock);

  if (f->ref < 1) {
    err_exit("fileclose: ref < 1");
  }

  if (--f->ref > 0) {
    pthread_spin_unlock(&ftable.lock);
    return;
  }

  struct inode *ip = f->ip;
  f->ref           = 0;
  pthread_spin_unlock(&ftable.lock);

  begin_op();
  iput(ip);
  end_op();
}

int filestat(struct file *f, struct stat *stbuf) {
  if (f->type == FD_INODE) {
    begin_op();
    ilock(f->ip);
    int res = stat_inode(f->ip, stbuf);
    iunlock(f->ip);
    end_op();
    return res;
  } else {
    err_exit("filestat: unknown file type");
    // unreachable
    return -1;
  }
}

int myfuse_getattr(const char *path, struct stat *stbuf,
                   struct fuse_file_info *fi) {
  (void)fi;
  begin_op();
  struct inode *ip = path2inode(path);
  int res          = 0;

  if (ip == NULL) {
    myfuse_debug_log("`%s' is not exist", path);
    end_op();
    res = -ENOENT;
    return res;
  }
  ilock(ip);
  res = stat_inode(ip, stbuf);
  iunlockput(ip);
  end_op();

  return res;
}

int myfuse_readdir(const char *path, void *buf, fuse_fill_dir_t filler,
                   off_t offset, struct fuse_file_info *fi,
                   enum fuse_readdir_flags flags) {
  if (fi == NULL) {
    return -ENOENT;
  }
  begin_op();
  struct inode *dp = ((struct file *)fi->fh)->ip;
  if (dp == NULL) {
    myfuse_debug_log("`%s' is not exist", path);
    end_op();
    return -ENOENT;
  }

  DEBUG_TEST(if (dp->ref < 1) { err_exit("myfuse_readdir: ref < 1"); });

  ilock(dp);

  struct dirent *de;
  char *dirbuf = malloc(dp->size);
  char file_name[DIRSIZE + 1];
  struct stat st;

  DEBUG_TEST(if (dp->type != T_DIR_INODE_MYFUSE) {
    free(dirbuf);
    iunlock(dp);
    end_op();
    return -EBADF;
  });

  if (inode_read_nbytes_locked(dp, dirbuf, dp->size, 0) != dp->size) {
    free(dirbuf);
    iunlock(dp);
    end_op();
    err_exit("dirlookup: failed to read dir");
  }

  for (int off = 0; off < dp->size; off += sizeof(*de)) {
    de = (struct dirent *)&dirbuf[off];
    if (de->inum == 0) {
      continue;
    }
    dirnamecpy(file_name, de->name);

    int stat_res = 0;
    if (de->inum != dp->inum) {
      stat_res = stat_inum(de->inum, &st);
    } else {
      stat_res = stat_inode(dp, &st);
    }
    if (stat_res == 0) {
      if (filler(buf, file_name, &st, 0, 0) != 0) {
        break;
      }
    }
  }

  iunlock(dp);
  free(dirbuf);
  end_op();

  return 0;
}

int myfuse_opendir(const char *path, struct fuse_file_info *fi) {
  begin_op();
  struct inode *dir_inode = path2inode(path);
  if (dir_inode == NULL) {
    end_op();
    return -ENOENT;
  }
  ilock(dir_inode);
  if (dir_inode->type != T_DIR_INODE_MYFUSE) {
    iunlockput(dir_inode);
    end_op();
    return -ENOTDIR;
  }
  struct file *file = filealloc();
  file->type        = FD_INODE;
  file->ip          = dir_inode;
  fi->fh            = (size_t)file;
  DEBUG_TEST(if (file->ip->ref < 1) { err_exit("myfuse_opendir: ref < 1"); });
  iunlock(dir_inode);
  end_op();
  return 0;
}

int myfuse_open(const char *path, struct fuse_file_info *fi) {
  begin_op();
  struct inode *file_inode = path2inode(path);
  if (file_inode == NULL) {
    if ((fi->flags & O_CREAT) == 0) {
      return -ENOENT;
    } else {
      // create the file
      char filename[DIRSIZE];
      struct inode *dir_inode = path2parentinode(path, filename);
      if (dir_inode == NULL) {
        end_op();
        return -ENOENT;
      }
      file_inode = ialloc(T_FILE_INODE_MYFUSE);
      file_inode->nlink++;
      iupdate(dir_inode);
      ilock(dir_inode);
      dirlink(dir_inode, filename, file_inode->inum);
      iunlockput(dir_inode);
    }
  }
  ilock(file_inode);
  // file type need not be checked. fuse will use getattr to check
  // open will only treat file
  struct file *file = filealloc();
  file->type        = FD_INODE;
  file->ip          = file_inode;
  if (fi->flags & O_RDONLY) {
    file->readable = 1;
    file->writable = 0;
  } else if (fi->flags & O_WRONLY) {
    file->readable = 0;
    file->writable = 1;
  } else if (fi->flags & O_RDWR) {
    file->readable = 1;
    file->writable = 1;
  } else {
    file->readable = 1;
    file->writable = 1;
  }

  fi->fh = (size_t)file;
  iunlock(file_inode);
  end_op();
  return 0;
}

static void release_internal(struct fuse_file_info *fi) {
  if (fi == NULL) {
    return;
  }
  struct file *file = (struct file *)fi->fh;
  if (file == NULL) {
    return;
  }
  fi->fh = 0;
  fileclose(file);
}

int myfuse_release(const char *path, struct fuse_file_info *fi) {
  release_internal(fi);
  return 0;
}

int myfuse_releasedir(const char *path, struct fuse_file_info *fi) {
  release_internal(fi);
  return 0;
}

int myfuse_mkdir(const char *path, mode_t mode) {
  int res = 0;
  char name[DIRSIZE];

  begin_op();

  struct inode *dp = path2parentinode(path, name);

  struct inode *ip = ialloc(T_DIR_INODE_MYFUSE);
  ilock(ip);

  ilock(dp);
  if (dirlink(dp, name, ip->inum) != 0) {
    res = -EEXIST;
    iunlockput(ip);
    end_op();
    return res;
  }
  iunlockput(dp);

  ip->nlink = 1;
  ip->perm  = mode;

  get_current_timespec(&ip->st_atimespec);
  ip->st_ctimespec = ip->st_mtimespec = ip->st_atimespec;

  iupdate(ip);
  iunlockput(ip);

  end_op();

  return res;
}

int myfuse_unlink(const char *path) {
  int res = 0;
  char name[DIRSIZE];
  struct dirent zero_de;
  uint poff;
  begin_op();

  memset(&zero_de, 0, sizeof(zero_de));

  struct inode *ip = path2inode(path);
  if (ip == NULL) {
    myfuse_debug_log("`%s' is not exist", path);
    end_op();
    return -ENOENT;
  }
  struct inode *dp = path2parentinode(path, name);

  DEBUG_TEST(assert(dp != NULL););

  ilock(dp);
  ilock(ip);

  if (ip->nlink == 0) {
    // dangling symbolic link
    iunlockput(dp);
    iunlockput(ip);
    end_op();
    return -ENOENT;
  }

  ip->nlink--;
  if (ip->nlink == 0) {
    struct inode *found_ip = NULL;
    if ((found_ip = dirlookup(dp, name, &poff)) != NULL) {
      inode_write_nbytes_locked(dp, (char *)&zero_de, sizeof(zero_de), poff);
      DEBUG_TEST(assert(found_ip->inum == ip->inum););
      iput(found_ip);
    }
  }
  iupdate(ip);
  iunlockput(ip);
  iunlockput(dp);

  end_op();

  return res;
}

int myfuse_rmdir(const char *path) {
  // we don't need to check if the path is a directory
  // fuse will first use getattr to check it
  int res = 0;
  char name[DIRSIZE];
  struct dirent zero_de;
  uint poff;

  memset(&zero_de, 0, sizeof(zero_de));

  begin_op();
  struct inode *ip = path2inode(path);

  if (ip == NULL) {
    myfuse_debug_log("`%s' is not exist", path);
    end_op();
    return -ENOENT;
  }

  if (ip->size != 0) {
    char *buf = malloc(ip->size);
    ilock(ip);
    if (inode_read_nbytes_locked(ip, buf, ip->size, 0) != ip->size) {
      iunlockput(ip);
      end_op();
      free(buf);
      err_exit("myfuse_rmdir: inode_read_nbytes_unlocked failed to read");
    }

    for (int i = 0; i < ip->size; i += sizeof(struct dirent)) {
      struct dirent *de = (struct dirent *)(buf + i);
      if (de->inum != 0) {
        myfuse_debug_log("myfuse_rmdir: `%s' is not empty", path);
        iunlockput(ip);
        end_op();
        free(buf);
        return -ENOTEMPTY;
      }
    }
    free(buf);
    iunlock(ip);
  }

  struct inode *dp = path2parentinode(path, name);
  ilock(dp);
  ip->nlink--;
  if (ip->nlink == 0) {
    if (dirlookup(dp, name, &poff) != NULL) {
      inode_write_nbytes_locked(dp, (char *)&zero_de, sizeof(zero_de), poff);
    }
  }
  iupdate(ip);

  iunlockput(dp);
  iunlockput(ip);
  end_op();

  return res;
}

int myfuse_read(const char *path, char *buf, size_t size, off_t offset,
                struct fuse_file_info *fi) {
  struct file *file = (struct file *)fi->fh;
  DEBUG_TEST(assert(file != NULL););
  int nbytes = inode_read_nbytes_unlocked(file->ip, buf, size, offset);
  return nbytes;
}

int myfuse_write(const char *path, const char *buf, size_t size, off_t offset,
                 struct fuse_file_info *fi) {
  struct file *file = (struct file *)fi->fh;
  DEBUG_TEST(assert(file != NULL););
  int nbytes = inode_write_nbytes_unlocked(file->ip, buf, size, offset);
  return nbytes;
}

int myfuse_truncate(const char *path, off_t size, struct fuse_file_info *fi) {
  (void)fi;
  begin_op();
  struct inode *ip = path2inode(path);

  if (ip == NULL) {
    end_op();
    return -ENOENT;
  }
  if (ip->type == T_DIR_INODE_MYFUSE) {
    end_op();
    return -EISDIR;
  }

  ilock(ip);
  itrunc2size(ip, size);
  iunlockput(ip);
  end_op();
  return 0;
}

int myfuse_access(const char *path, int mask) {
  (void)mask;
  begin_op();
  struct inode *ip = path2inode(path);
  if (ip == NULL) {
    return -ENOENT;
  }
  iput(ip);
  end_op();

  return 0;
}

int myfuse_create(const char *path, mode_t mode, struct fuse_file_info *fi) {
  if (!(mode & S_IFREG)) {
    // must be a regular file
    // shouldn't reach
    err_exit("must be regular file");
  }

  begin_op();
  // create the file
  char filename[DIRSIZE];
  struct inode *dir_inode = path2parentinode(path, filename);
  if (dir_inode == NULL) {
    end_op();
    return -ENOENT;
  }
  struct inode *file_inode = ialloc(T_FILE_INODE_MYFUSE);
  ilock(file_inode);
  file_inode->nlink++;
  file_inode->perm = mode & 0777;

  get_current_timespec(&file_inode->st_atimespec);
  file_inode->st_ctimespec = file_inode->st_mtimespec =
      file_inode->st_atimespec;

  iupdate(file_inode);
  ilock(dir_inode);
  dirlink(dir_inode, filename, file_inode->inum);
  iunlockput(dir_inode);

  // open the file
  struct file *file = filealloc();
  file->type        = FD_INODE;
  file->ip          = file_inode;
  if (mode & O_RDONLY) {
    file->readable = 1;
    file->writable = 0;
  } else if (mode & O_WRONLY) {
    file->readable = 0;
    file->writable = 1;
  } else if (mode & O_RDWR) {
    file->readable = 1;
    file->writable = 1;
  } else {
    file->readable = 1;
    file->writable = 1;
  }

  fi->fh = (size_t)file;
  iunlock(file_inode);
  end_op();

  return 0;
}

int myfuse_chmod(const char *path, mode_t mode, struct fuse_file_info *fi) {
  (void)fi;
  begin_op();
  struct inode *ip = path2inode(path);
  if (ip == NULL) {
    return -ENOENT;
  }

  ilock(ip);
  ip->perm = mode & 0777;
  iupdate(ip);
  iunlockput(ip);

  end_op();

  return 0;
}

off_t myfuse_lseek(const char *path, off_t off, int whence,
                   struct fuse_file_info *fi) {
  (void)path;
  struct file *f = (struct file *)fi->fh;
  off_t result;
  DEBUG_TEST(assert(f != NULL););

  ilock(f->ip);
  // FIXME: check if overflow will occur
  switch (whence) {
    case SEEK_SET:
      f->off = off;
      result = f->off;
      break;
    case SEEK_CUR:
      f->off += off;
      result = f->off;
      break;
    case SEEK_END:
      f->off = f->ip->size + off;
      result = f->off;
      break;
    default:
      result = -EINVAL;
      break;
  }
  iunlock(f->ip);
  return result;
}

int myfuse_rename(const char *from, const char *target, unsigned int flags) {
  char target_name[DIRSIZE];
  char from_name[DIRSIZE];
  struct dirent zero_de;
  uint poff;
  int res = 0;

  memset(&zero_de, 0, sizeof(zero_de));

  begin_op();
  struct inode *target_ip = path2inode(target);
  struct inode *target_dp = path2parentinode(target, target_name);
  struct inode *from_ip   = path2inode(from);
  struct inode *from_dp   = path2parentinode(from, from_name);
  if ((target_ip == NULL && target_dp == NULL) || from_ip == NULL ||
      from_dp == NULL) {
    return -ENOENT;
  }

  if (from_dp == target_dp) {
    // FIXME: check if here implemented right
    // rename in the same directory
    ilock(from_ip);
    ilock(from_dp);
    iput(dirlookup(from_dp, from_name, &poff));
    size_t name_len = strlen(target_name) + 1;  // need copy the null terminator
    name_len > DIRSIZE ? name_len = DIRSIZE : name_len;
    inode_write_nbytes_locked(target_dp, target_name, name_len,
                              poff + (size_t) & ((struct dirent *)0)->name);
    iunlock(from_dp);
    iunlock(from_ip);
  } else {
    ilock(from_ip);
    ilock(from_dp);
    // unlink the source
    iput(dirlookup(from_dp, from_name, &poff));
    // unlink from the from_dp
    inode_write_nbytes_locked(from_dp, (char *)&zero_de, sizeof(zero_de), poff);
    iunlock(from_dp);
    iunlock(from_ip);

    if (target_ip == NULL) {
      ilock(target_dp);
      dirlink(target_dp, target_name, from_ip->inum);
      iunlock(target_dp);
    } else {
      // target exists
      if (target_ip->type == T_DIR_INODE_MYFUSE) {
        // target is a directory
        // link under the directory
        ilock(target_ip);
        dirlink(target_ip, from_name, from_ip->inum);
        iunlock(target_ip);
      } else {
        if (flags & RENAME_EXCHANGE) {
          DEBUG_TEST(assert(target_dp == NULL););
          ilock(target_dp);
          ilock(target_ip);

          // unlink from target_dp
          iput(dirlookup(target_dp, target_name, &poff));
          inode_write_nbytes_locked(target_dp, (char *)&zero_de,
                                    sizeof(zero_de), poff);

          dirlink(target_dp, from_name, from_ip->inum);
          dirlink(from_dp, from_name, target_ip->inum);

          iunlock(target_ip);
          iunlock(target_dp);
        } else if (flags & RENAME_NOREPLACE) {
          // just end op
          res = -EEXIST;
        }
      }
    }
  }

  if (target_ip != NULL) {
    iput(target_ip);
  }
  if (target_dp != NULL) {
    iput(target_dp);
  }
  if (from_ip != NULL) {
    iput(from_ip);
  }
  if (from_dp != NULL) {
    iput(from_dp);
  }

  end_op();
  return res;
}

#include "block_allocator.h"

int myfuse_statfs(const char *path, struct statvfs *buf) {
  buf->f_blocks = MYFUSE_STATE->sb.nblocks;
  buf->f_bsize  = BSIZE;

  fsblkcnt_t free_blocks = 0;
  for (int i = 0; i < MYFUSE_STATE->sb.size; i++) {
    if (bmap_block_statue_get(i) == 0) {
      free_blocks++;
    }
  }
  buf->f_bfree   = free_blocks;
  buf->f_fsid    = FSMAGIC;
  buf->f_namemax = DIRSIZE;
  return 0;
}
