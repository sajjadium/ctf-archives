#!/usr/bin/env bash
mkdir -p /sys/fs/cgroup/{cpu,memory,pids}/NSJAIL
chown inmate /sys/fs/cgroup/{cpu,memory,pids}/NSJAIL
nsjail --config $1 --user inmate --group inmate -- $2
