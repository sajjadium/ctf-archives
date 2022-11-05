#include "block_device.h"
#include <fcntl.h>
#include <unistd.h>
#include <pthread.h>
#include "util.h"

// NOTE: after the read and write need be protected by locks as after the lseek
// before the write the read-write position may be changed by other threads
static pthread_mutex_t disk_lock;

static int device_fd;

static int write_block_raw_byfd(int fd, uint block_id, const u_char *buf) {
#ifdef DEBUG
  if (MYFUSE_STATE != NULL) {
    if (block_id >= MYFUSE_STATE->sb.size) {
      err_exit("write out side of disk");
    }
  }
#endif
  pthread_mutex_lock(&disk_lock);
  if (lseek(fd, block_id * BSIZE, SEEK_SET) != block_id * BSIZE) {
    return -1;
  }
  int nbytes = write(fd, buf, BSIZE);
  pthread_mutex_unlock(&disk_lock);
  return nbytes;
}

int write_block_raw(uint block_id, const u_char *buf) {
  return write_block_raw_byfd(device_fd, block_id, buf);
}

static int read_block_raw_byfd(int fd, uint block_id, u_char *buf) {
#ifdef DEBUG
  if (MYFUSE_STATE != NULL) {
    if (block_id >= MYFUSE_STATE->sb.size) {
      err_exit("read out side of disk");
    }
  }
#endif
  pthread_mutex_lock(&disk_lock);
  if (lseek(fd, block_id * BSIZE, SEEK_SET) != block_id * BSIZE) {
    return -1;
  }
  int nbytes = read(fd, buf, BSIZE);
  pthread_mutex_unlock(&disk_lock);
  return nbytes;
}

int read_block_raw(uint block_id, u_char *buf) {
  return read_block_raw_byfd(device_fd, block_id, buf);
}

static int read_block_raw_nbytes_byfd(int fd, uint block_id, u_char *buf,
                                      uint nbytes) {
#ifdef DEBUG
  if (MYFUSE_STATE != NULL) {
    if (block_id > MYFUSE_STATE->sb.size) {
      err_exit("read out side of disk");
    }
  }
#endif
  pthread_mutex_lock(&disk_lock);
  if (lseek(fd, block_id * BSIZE, SEEK_SET) != block_id * BSIZE) {
    return -1;
  }
  if (nbytes > BSIZE) {
    nbytes = BSIZE;
  }
  int nbytes_read = read(fd, buf, nbytes);
  pthread_mutex_unlock(&disk_lock);
  return nbytes_read;
}

int read_block_raw_nbytes(uint block_id, u_char *buf, uint nbytes) {
  return read_block_raw_nbytes_byfd(device_fd, block_id, buf, nbytes);
}

void block_device_init(const char *path_to_device) {
  device_fd = open(path_to_device, O_RDWR);
  if (device_fd < 0) {
    err_exit("failed to open disk %s", path_to_device);
  }
  pthread_mutex_init(&disk_lock, NULL);
}
