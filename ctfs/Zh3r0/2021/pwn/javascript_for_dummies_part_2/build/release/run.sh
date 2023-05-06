#!/bin/bash
LD_PRELOAD=./libjemalloc.so.2 ./mujs $1
