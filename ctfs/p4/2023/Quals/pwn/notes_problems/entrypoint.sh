#!/bin/bash

mkdir -p /sys/fs/cgroup/{cpu,memory,pids}/NSJAIL

exec nsjail \
    --mode l \
    --port 4000 \
    --user 65534:65534 \
    --group 65534:65534 \
    --chroot / \
    --cwd /home/notes \
    --time_limit 60 \
    -T /tmp \
    -E LC_ALL \
    -- /home/notes/notes
