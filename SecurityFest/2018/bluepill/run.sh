#! /usr/bin/env bash

qemu-system-x86_64 -kernel ./tiny.kernel -initrd ./init -m 32 -nographic -append "console=ttyS0"