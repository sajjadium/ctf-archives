#!/bin/bash
arm-linux-gnueabi-gcc -g -static -Iinclude -o chal chal.c libcapstone.a
