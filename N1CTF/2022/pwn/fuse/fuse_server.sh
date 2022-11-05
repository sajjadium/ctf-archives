#!/bin/sh

# this script will watch your fuse server, if you crash the fuse filesystem, it will simulate a system reboot by restarting the fuse server

temp_dir=$1
until /usr/bin/myfuse --device_path=${temp_dir}/cfs.disk ${temp_dir}/tmp/cfs -s -d -o allow_other; do
  echo "myfuse crashed with exit code $?. Respawning.." >&2
  fusermount -u ${temp_dir}/tmp/cfs
  sleep 1
done
