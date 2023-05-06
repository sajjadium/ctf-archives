#!/bin/bash
unset LD_LIBRARY_PATH
PWD=/home/echo
qemu-arm -L ./ ./echo

