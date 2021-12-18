#!/bin/bash
set -euo pipefail
export NAME="$(< /dev/urandom tr -dc a-zA-Z0-9 | head -c 24)"
export HOME="/home/ctf"

exec ./lkvm \
run \
-k ./bzImage \
-m 128 \
-c 1 \
--initrd ./initramfs.cpio \
--params "root=/init" \
--rng \
--console virtio \
--balloon \
--name "$NAME"
