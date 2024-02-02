#!/bin/sh

mount -o rw,remount /dev
mkdir /dev/pts
mount -o ro,remount /dev
