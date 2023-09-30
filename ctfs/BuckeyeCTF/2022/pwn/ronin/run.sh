#!/bin/bash
echo "Starting NSJAIL"
mkdir /sys/fs/cgroup/{cpu,memory,pids}/NSJAIL
chown ctf /sys/fs/cgroup/{cpu,memory,pids}/NSJAIL
nsjail --config /jail.cfg --user ctf --group ctf