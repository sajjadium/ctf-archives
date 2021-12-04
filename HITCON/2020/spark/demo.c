/*
 * This is a demo program to show how to interact with SPARK.
 * Don't waste time on finding bugs here ;)
 *
 * Copyright (c) 2020 david942j
 */

#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <unistd.h>

#include <linux/spark.h>

#define DEV_PATH "/dev/node"

#define N 6
static int fd[N];
const char l[] = "ABCDEF";

/*
    B -- 10 -- D -- 11 -- F
   / \         |
  4   |        |
 /    |        |
A     5        4
 \    |        |
  2   |        |
    \ |        |
      C -- 3 - E
 */
static void link(int a, int b, unsigned int weight) {
  printf("Creating link between '%c' and '%c' with weight %u\n", l[a], l[b], weight);
  assert(ioctl(fd[a], SPARK_LINK, fd[b] | ((unsigned long long) weight << 32)) == 0);
}

static void query(int a, int b) {
  struct spark_ioctl_query qry = {
    .fd1 = fd[a],
    .fd2 = fd[b],
  };
  assert(ioctl(fd[0], SPARK_QUERY, &qry) == 0);
  printf("The length of shortest path between '%c' and '%c' is %lld\n", l[a], l[b], qry.distance);
}

int main(int argc, char *argv[]) {
  for (int i = 0; i < N; i++) {
    fd[i] = open(DEV_PATH, O_RDONLY);
    assert(fd[i] >= 0);
  }
  link(0, 1, 4);
  link(0, 2, 2);
  link(1, 2, 5);
  link(1, 3, 10);
  link(2, 4, 3);
  link(3, 4, 4);
  link(3, 5, 11);
  assert(ioctl(fd[0], SPARK_FINALIZE) == 0);
  query(0, 5);
  query(3, 2);
  query(2, 5);

  for (int i = 0; i < N; i++)
    close(fd[i]);
  return 0;
}
