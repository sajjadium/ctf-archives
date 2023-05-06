// SPDX-License-Identifier: Apache-2.0
/*
 * Copyright 2021 Google LLC.
 */

#define _GNU_SOURCE

#include <grp.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
	if (setgid(1)) {
		perror("setgid");
		return 1;
	}

	if (setgroups(0, NULL)) {
		perror("setgroups");
		return 1;
	}

	if (setuid(1)) {
		perror("setuid");
		return 1;
	}

	putchar('\n');
	system("/usr/bin/resize > /dev/null");
	execl("/bin/sh", "sh", NULL);

	perror("execl");
	return 1;
}
