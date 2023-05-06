// SPDX-License-Identifier: MIT
/*
 * Copyright 2021 Google LLC.
 *
 * This file is for you to explore how LLVM eBPF assembly look like
 * for various different constructs, considering that you will need
 * to hand-write assembly for this challenge.
 *
 * See examples of eBPF C code:
 * https://github.com/torvalds/linux/tree/master/samples/bpf
 * Compile with:
 * clang -target bpf -Wall -pipe -O2 -D__x86_64__ -S test.bpf.c -o test.bpf.S
 */

#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>

SEC("socket")
int prog(struct __sk_buff *ctx)
{
	return 0;
}

char _license[] SEC("license") = "GPL";
