#!/bin/bash

LD_PRELOAD="./libc-2.31.so ./libseccomp.so.2.5.1" ./ld-2.31.so ./vuln
