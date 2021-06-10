#define _GNU_SOURCE

#include <err.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>
#include <sys/types.h>

#include "libcheck.h"

__attribute__((aligned(4096))) uint8_t (*_xor)(uint8_t, uint8_t);
__attribute__((aligned(4096))) uint8_t (*_or)(uint8_t, uint8_t);

void shuffle(size_t *array, size_t n)
{
  if (n == 0) {
    return;
  }

  for (size_t i = 0; i < n - 1; i++) {
    size_t j = i + rand() / (RAND_MAX / (n - i) + 1);
    size_t t = array[j];
    array[j] = array[i];
    array[i] = t;
  }
}

static void read_secret(uint8_t *secret, size_t size)
{
  FILE *fp;

  fp = fopen("secret.txt", "r");
  if (fp == NULL) {
    err(1, "fopen");
  }

  if (fgets((char *)secret, size, fp) == NULL) {
    err(1, "fread");
  }

  fclose(fp);
}

bool check_secret(uint8_t *p, size_t size)
{
  uint8_t secret[SECRET_SIZE+1];
  size_t indexes[SECRET_SIZE];

  if (size != SECRET_SIZE) {
    return false;
  }

  /* randomize access to secret to prevent template attacks */
  for (size_t i = 0; i < size; i++) {
    indexes[i] = i;
  }
  shuffle(indexes, size);

  read_secret(secret, size+1);

  uint8_t ret = 0;
  for (size_t i = 0; i < size; i++) {
    size_t index = indexes[i];
    uint8_t tmp;

    tmp = _xor(secret[index], p[index]);
    ret = _or(ret, tmp);
  }

  return ret == 0;
}
