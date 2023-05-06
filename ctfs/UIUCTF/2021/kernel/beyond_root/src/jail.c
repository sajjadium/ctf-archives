// SPDX-License-Identifier: Apache-2.0
/*
 * Copyright 2021 Google LLC.
 */

#define _GNU_SOURCE

#include <grp.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mount.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
	putchar('\n');
	system("/usr/bin/resize > /dev/null");
	execl("/bin/sh", "sh", NULL);

	perror("execl");
	return 1;
}
