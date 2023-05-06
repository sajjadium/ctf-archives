# Copyright 2021 Google LLC.
# SPDX-License-Identifier: MIT

.PHONY: clean
.SECONDARY:
.DELETE_ON_ERROR:

BPFTOOL ?= bpftool

all: bpf

%.bpf.o: %.bpf.S
	llvm-mc -triple bpf -filetype=obj $< -o $@
	llvm-strip -g $@

%.skel.h: %.bpf.o
	$(BPFTOOL) gen skeleton $< > $@

bpf: bpf.c bpf.skel.h
	gcc -static -Wall -pipe -O2 -g $< -o $@ -lbpf -lelf -lz

clean:
	rm -rf bpf *.o *.skel.h
