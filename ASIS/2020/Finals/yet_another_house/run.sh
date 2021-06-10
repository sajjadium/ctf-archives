#!/bin/bash
./ynetd -p 10111 "LD_PRELOAD=./libc-2.32.so ./house-of-yet_another_house"
