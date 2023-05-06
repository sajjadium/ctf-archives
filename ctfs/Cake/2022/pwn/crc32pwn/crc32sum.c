#include <ctype.h>
#include <fcntl.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/file.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

/**
 * Calculate CRC32 hash for data
 */
unsigned int crc32(unsigned char *data, size_t size)
{
  size_t i, j;
  unsigned int hash;

  hash = 0xFFFFFFFF;
  for (i = 0; i < size; i++) {
    hash ^= data[i];
    for (j = 0; j < CHAR_BIT; j++) {
      if (hash & 1)
        hash = (hash >> 1) ^ 0xEDB88320;
      else
        hash >>= 1;
    }
  }

  return hash ^ 0xFFFFFFFF;
}

/**
 * Calculate CRC32 hash for file
 */
void crc32sum(const char *filepath)
{
  int fd;
  char *buffer, *p;
  struct stat stbuf;

  /* Try to open file */
  if ((fd = open(filepath, O_RDONLY)) < 0) {
    perror(filepath);
    return;
  }

  /* Lock file */
  if (flock(fd, LOCK_SH)) {
    perror("flock");
    return;
  }

  /* Get file size */
  if (fstat(fd, &stbuf)) {
    perror(filepath);
    flock(fd, LOCK_UN);
    return;
  }

  /* Allocate buffer */
  if (!(buffer = malloc(stbuf.st_size))) {
    perror("Memory Error");
    flock(fd, LOCK_UN);
    return;
  }

  /* Read file */
  p = buffer;
  while (read(fd, p++, 1) == 1);

  /* Calculate hash */
  printf("%s: %08x\n", filepath, crc32(buffer, stbuf.st_size));

  /* Cleanup */
  free(buffer);
  flock(fd, LOCK_UN);
  close(fd);
}

/**
 * Entry point
 */
int main(int argc, char **argv)
{
  char *filepath;

  setreuid(geteuid(), geteuid());

  if (argc < 2) {
    printf("Usage: %s <file> ...\n", argv[0]);
    if (system("/usr/bin/which crc32 > /dev/null") == 0)
      puts("Your system has `crc32` too");
    return 1;
  }

  for (int i = 1; i < argc; i++) {
    filepath = strdup(argv[i]);
    crc32sum(filepath);
    free(filepath);
  }

  return 0;
}
