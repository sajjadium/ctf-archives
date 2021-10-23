#!/bin/bash
mkdir -p /sys/fs/cgroup/{cpu,memory,pids}/NSJAIL
chown ctf /sys/fs/cgroup/{cpu,memory,pids}/NSJAIL
nsjail --config /jail.cfg --user ctf --group ctf
