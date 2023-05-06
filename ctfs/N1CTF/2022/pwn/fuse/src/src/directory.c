#include "directory.h"
#include <pthread.h>
#include <malloc.h>
#include <inode.h>
#include <assert.h>

static int dirnamecmp(const char* a, const char* b) {
  return strncmp(a, b, DIRSIZE);
}

void dirnamencpy(char* a, const char* b) { memmove(a, b, DIRSIZE); }

void dirnamecpy(char* a, const char* b) { strcpy(a, b); }

struct inode* dirlookup(struct inode* dp, const char* name, uint* poff) {
  struct dirent* de;
  char* buf = malloc(dp->size);

  DEBUG_TEST(
      if (dp->type != T_DIR_INODE_MYFUSE) {
        free(buf);
        err_exit("dirlookup: file is not a dir");
      }

      // pthread_mutex_trylock: return 0 if not locked
      if (!pthread_mutex_trylock(&dp->lock)) {
        free(buf);
        err_exit("dirlookup: dp is not locked");
      });

  if (inode_read_nbytes_locked(dp, buf, dp->size, 0) != dp->size) {
    free(buf);
    err_exit("dirlookup: failed to read dir");
  }

  for (int off = 0; off < dp->size; off += sizeof(*de)) {
    de = (struct dirent*)&buf[off];
    if (de->inum == 0) {
      continue;
    }
    if (dirnamecmp(de->name, name) == 0) {
      if (poff) {
        *poff = off;
      }
      uint inum = de->inum;
      free(buf);
      return iget(inum);
    }
  }

  free(buf);
  return NULL;
}

int dirlink(struct inode* dp, const char* name, uint inum) {
  int off           = 0;
  struct dirent* de = NULL;
  struct inode* ip;

  DEBUG_TEST(
      // pthread_mutex_trylock: return 0 if not locked
      if (!pthread_mutex_trylock(&dp->lock)) {
        err_exit("dirlink called with unlocked inode");
      }

      // test the inode is a directory
      if (dp->type != T_DIR_INODE_MYFUSE) {
        err_exit("dirlink called with non-directory inode");
      }

      // test the directory size
      if (dp->size % sizeof(struct dirent) != 0) {
        err_exit("dirlink called with directory inode with invalid size");
      });

  // Check that name is not present.
  if ((ip = dirlookup(dp, name, 0)) != 0) {
    iput(ip);
    return -1;
  }

  // Look for an empty dirent.
  // this is a userland program, we can do this to save time
  char* buf = NULL;
  if (dp->size) {
    buf = malloc(dp->size);
    if (inode_read_nbytes_locked(dp, buf, dp->size, 0) != dp->size) {
      free(buf);
      err_exit("dirlink: read failed");
    }
    for (off = 0; off < dp->size; off += sizeof(*de)) {
      de = (struct dirent*)&buf[off];
      if (de->inum == 0) break;
    }
  } else {
    buf = malloc(sizeof(*de));
    de  = (struct dirent*)buf;
  }

  strncpy(de->name, name, DIRSIZE);
  de->inum = inum;
  if (inode_write_nbytes_locked(dp, (char*)de, sizeof(*de), off) !=
      sizeof(*de)) {
    free(buf);
    err_exit("dirlink: write entry failed");
  }

  free(buf);

  return 0;
}

// Paths

// Copy the next path element from path into name.
// Return a pointer to the element following the copied one.
// The returned path has no leading slashes,
// so the caller can check *path=='\0' to see if the name is the last one.
// If no name to remove, return 0.
//
// Examples:
//   skipelem("a/bb/c", name) = "bb/c", setting name = "a"
//   skipelem("///a//bb", name) = "bb", setting name = "a"
//   skipelem("a", name) = "", setting name = "a"
//   skipelem("", name) = skipelem("////", name) = 0
//
static const char* skipelem(const char* path, char* name) {
  const char* s;
  int len;

  while (*path == '/') path++;
  if (*path == 0) return 0;
  s = path;
  while (*path != '/' && *path != 0) path++;
  len = path - s;
  if (len >= DIRSIZE)
    memmove(name, s, DIRSIZE);
  else {
    memmove(name, s, len);
    name[len] = 0;
  }
  while (*path == '/') path++;
  return path;
}

const char* skiptoend(const char* path) {
  char name[DIRSIZE];
  const char* elem;
  const char* last_elem;
  for (elem = skipelem(path, name); elem; elem = skipelem(elem, name)) {
    last_elem = elem;
  }

  DEBUG_TEST(assert(dirnamecmp(last_elem, name) == 0););

  return last_elem;
}

// Look up and return the inode for a path name.
// If parent != 0, return the inode for the parent and copy the final
// path element into name, which must have room for DIRSIZ bytes.
// Must be called inside a transaction since it calls iput().
static struct inode* namex(const char* path, int nameiparent, char* name) {
  struct inode *ip, *next;

  if (*path == '/')
    ip = iget(ROOTINO);
  else
    err_exit("cwd not implemented");

  while ((path = skipelem(path, name)) != 0) {
    ilock(ip);
    if (ip->type != T_DIR_INODE_MYFUSE) {
      iunlockput(ip);
      return 0;
    }
    if (nameiparent && *path == '\0') {
      // Stop one level early.
      iunlock(ip);
      return ip;
    }
    if ((next = dirlookup(ip, name, 0)) == 0) {
      iunlockput(ip);
      return 0;
    }
    iunlockput(ip);
    ip = next;
  }
  if (nameiparent) {
    iput(ip);
    return 0;
  }
  return ip;
}

struct inode* path2inode(const char* path) {
  char name[DIRSIZE];
  return namex(path, 0, name);
}

struct inode* path2parentinode(const char* path, char* name) {
  return namex(path, 1, name);
}
