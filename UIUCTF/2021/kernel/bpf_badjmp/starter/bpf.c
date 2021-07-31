// SPDX-License-Identifier: MIT
/*
 * Copyright 2021 Google LLC.
 */

#include <stdlib.h>

#include "bpf.skel.h"

int main(int argc, char *argv[])
{
	struct bpf_bpf *obj = bpf_bpf__open_and_load();
	if (!obj)
		exit(1);

	// Your code here

	return 0;
}
