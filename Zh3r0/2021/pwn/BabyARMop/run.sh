#!/usr/bin/env bash

socat tcp-listen:1337,fork,reuseaddr exec:"/chroot/qemu-aarch64 -L /chroot -nx /chroot/vuln"
